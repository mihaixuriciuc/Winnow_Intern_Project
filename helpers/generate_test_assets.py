import cv2
import numpy as np
import os


def create_dummy_video(folder_path, filename, text, bg_color):
    """
    Creates a 3-second dummy mp4 video with a solid background and centered text.
    """
    # Ensure the target directory exists
    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join(folder_path, filename)

    # Video specs: 640x480 resolution, 30 FPS, 3 seconds long
    width, height = 640, 480
    fps = 30
    duration = 3

    # Set up the video writer (mp4 format)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))

    for _ in range(fps * duration):
        # Create a blank frame with the background color (OpenCV uses BGR)
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = bg_color

        # Add the identifying text to the center
        cv2.putText(frame, text, (30, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

        out.write(frame)

    out.release()
    print(f"Created: {filepath}")


# --- Dynamically set the Base Directory based on your folder structure ---
# This gets the absolute path of the 'helpers' folder where this script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Point BASE_DIR to: helpers/winnow-automation/test_videos/assets
BASE_DIR = os.path.join(SCRIPT_DIR, 'winnow-automation', 'test_videos', 'assets')

# Define scenarios (Colors are BGR: Blue, Green, Red)
scenarios = [
    # 1. Single Items
    (os.path.join(BASE_DIR, "single_item"), "apple_center_drop.mp4", "APPLE CENTER", (0, 0, 200)),
    (os.path.join(BASE_DIR, "single_item"), "bottle_edge_drop.mp4", "BOTTLE EDGE", (200, 0, 0)),

    # 2. Multiple Items
    (os.path.join(BASE_DIR, "multiple_items"), "apple_and_bottle.mp4", "APPLE + BOTTLE", (200, 100, 0)),

    # 3. Edge Cases
    (os.path.join(BASE_DIR, "edge_cases"), "low_light_apple.mp4", "LOW LIGHT APPLE", (0, 0, 50)),
    (os.path.join(BASE_DIR, "edge_cases"), "motion_blur_bottle.mp4", "BLURRY BOTTLE", (100, 0, 0)),

    # 4. Negative Tests
    (os.path.join(BASE_DIR, "negative_tests"), "non_throwable_object.mp4", "EMPTY HANDS", (50, 50, 50)),
    (os.path.join(BASE_DIR, "negative_tests"), "non_garbage_item.mp4", "NON GARBAGE", (0, 150, 150))
]

print(f"Targeting Asset Directory: {BASE_DIR}")
print("Generating Test Assets...")

for folder, filename, text, color in scenarios:
    create_dummy_video(folder, filename, text, color)

print("\nSuccess! Your dummy test bed is ready in the 'assets' folder.")