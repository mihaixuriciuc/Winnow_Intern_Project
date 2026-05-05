import os
import subprocess
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import threading


# Track the video player process so we can kill it
current_process = None
current_scenario = None  # Add this to remember what is playing

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(BASE_DIR, 'test_videos', 'assets')
VLC_PATH = '/Applications/VLC.app/Contents/MacOS/VLC' # put here the path to your vlc


def run_playlist_worker(video_list):
    """Background task that plays videos one by one and updates the tracker."""
    global current_process, current_scenario

    for video_path in video_list:
        # Update the tracker so your /current endpoint knows exactly what is on screen
        current_scenario = os.path.relpath(video_path, ASSET_DIR).replace('\\', '/')

        command = ['/Applications/VLC.app/Contents/MacOS/VLC', '--fullscreen', '--play-and-exit',
                   '--no-video-title-show', video_path]

        # Start the video
        current_process = subprocess.Popen(command)

        # CRITICAL: Tell Python to wait here until VLC finishes the current video
        current_process.wait()

    # When the loop finishes, reset the environment
    current_scenario = None
    current_process = None

def get_scenarios(request):
    """Returns all available test videos found in the assets folder."""
    scenarios = []

    # We will check if the directory actually exists
    path_exists = os.path.exists(ASSET_DIR)

    if path_exists:
        for root, dirs, files in os.walk(ASSET_DIR):
            for file in files:
                if file.endswith(".mp4"):
                    rel_dir = os.path.relpath(root, ASSET_DIR)
                    scenarios.append(os.path.join(rel_dir, file).replace('\\', '/'))

    # Return the debugging info right in the browser!
    return JsonResponse({
        "1_LOOKING_IN_THIS_EXACT_FOLDER": ASSET_DIR,
        "2_DOES_FOLDER_EXIST": path_exists,
        "3_AVAILABLE_SCENARIOS": scenarios
    })


@csrf_exempt
def play_video(request):
    """Starts playing a requested video file."""
    global current_process

    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    if current_process and current_process.poll() is None:
        return JsonResponse({"error": "System Busy: A video is already playing."}, status=409)

    try:
        data = json.loads(request.body)
        scenario_path = data.get('scenario')

        full_path = os.path.abspath(os.path.join(ASSET_DIR, scenario_path))

        if not os.path.exists(full_path):
            return JsonResponse({"error": f"File not found: {full_path}"}, status=404)

        global current_scenario
        current_scenario = scenario_path

        vlc_path = VLC_PATH
        current_process = subprocess.Popen([
            vlc_path, '--fullscreen', '--play-and-exit', '--no-video-title-show', full_path
        ])

        return JsonResponse({"status": "Playing", "scenario": scenario_path})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def play_all(request):
    """Gathers all videos and starts the background playback queue."""
    global current_process

    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    if current_process and current_process.poll() is None:
        return JsonResponse({"error": "System Busy: Stop current playback first."}, status=409)

    try:
        # 1. Gather every single .mp4 file in your assets folder
        all_videos = []
        for root, dirs, files in os.walk(ASSET_DIR):
            for file in files:
                if file.endswith(".mp4"):
                    all_videos.append(os.path.abspath(os.path.join(root, file)))

        if not all_videos:
            return JsonResponse({"error": "No videos found in assets folder."}, status=404)

        # 2. Hand the list off to the background thread
        # We use a daemon thread so it doesn't block Django from returning the HTTP response instantly
        threading.Thread(target=run_playlist_worker, args=(all_videos,), daemon=True).start()

        return JsonResponse({
            "status": "Playing All Videos",
            "total_scenarios": len(all_videos)
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def play_specific(request, scenario_path):
    """Plays a specific video directly from the URL path."""
    global current_process

    # Auto-kill previous video if it's still running
    if current_process and current_process.poll() is None:
        current_process.terminate()

    full_path = os.path.abspath(os.path.join(ASSET_DIR, scenario_path))

    if not os.path.exists(full_path):
        return JsonResponse({"error": f"File not found: {full_path}"}, status=404)

    global current_scenario
    current_scenario = scenario_path

    try:
        vlc_path = '/Applications/VLC.app/Contents/MacOS/VLC'
        current_process = subprocess.Popen([
            vlc_path, '--fullscreen', '--play-and-exit', '--no-video-title-show', full_path
        ])

        return JsonResponse({"status": "Playing Direct URL", "scenario": scenario_path})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_current_video(request):
    """Returns the currently playing video, or IDLE if nothing is playing."""
    global current_process, current_scenario

    # Check if a video is actively running
    if current_process and current_process.poll() is None:
        return JsonResponse({
            "state": "PLAYING",
            "scenario": current_scenario
        })
    else:
        # If the video finished naturally, clear the tracker
        current_scenario = None
        return JsonResponse({
            "state": "IDLE",
            "scenario": None
        })


@csrf_exempt
def play_random(request):
    """Queues up all videos and plays them in a completely random order."""
    global current_process

    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    if current_process and current_process.poll() is None:
        return JsonResponse({"error": "System Busy: Stop current playback first."}, status=409)

    try:
        # 1. Gather every single .mp4 file
        all_videos = []
        for root, dirs, files in os.walk(ASSET_DIR):
            for file in files:
                if file.endswith(".mp4"):
                    all_videos.append(os.path.abspath(os.path.join(root, file)))

        if not all_videos:
            return JsonResponse({"error": "No videos found."}, status=404)

        # 2. THE MAGIC: Shuffle the list randomly
        random.shuffle(all_videos)

        # 3. Prepare and fire the VLC command
        vlc_path = '/Applications/VLC.app/Contents/MacOS/VLC'
        command = [vlc_path, '--fullscreen', '--play-and-exit', '--no-video-title-show']
        command.extend(all_videos)

        current_process = subprocess.Popen(command)

        return JsonResponse({
            "status": "Playing Random Playlist",
            "total_scenarios": len(all_videos),
            "play_order": all_videos  # Returns the exact random order chosen
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def stop_video(request):
    """Kills the video player."""
    global current_process
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    if current_process and current_process.poll() is None:
        current_process.terminate()
        current_process = None
        global current_scenario
        current_scenario = None  # CLEAR IT HERE
        return JsonResponse({"status": "Stopped"})

    return JsonResponse({"status": "Idle. Nothing was playing."})


