# Winnow_Intern_Project
this will be the repository for the task given by winnow team

So this is the README file for this project, ill try to be as concise as possible.

First of all, using this command I created some test videos so I can verify that the api is woring properly, and also some fictive test cases for the model:

```
# Ensure the folders exist
mkdir -p test_videos/assets/single_item
mkdir -p test_videos/assets/multiple_items
mkdir -p test_videos/assets/edge_cases
mkdir -p test_videos/assets/negative_tests

# Download a small, free sample video into each folder
curl -o test_videos/assets/single_item/apple_center_drop.mp4 https://www.w3schools.com/html/mov_bbb.mp4
curl -o test_videos/assets/multiple_items/apple_and_bottle.mp4 https://www.w3schools.com/html/mov_bbb.mp4
curl -o test_videos/assets/edge_cases/low_light_apple.mp4 https://www.w3schools.com/html/mov_bbb.mp4
curl -o test_videos/assets/negative_tests/empty_hands.mp4 https://www.w3schools.com/html/mov_bbb.mp4
```

Then I created these  endpoints, in this order:

- one endpoint that shows all the scenarios available (api/scenarios)
- one endpoint (api/play) that can play a specific video or a specific scenario folder at once, this requires the following json body:
```
{
  "scenario": "multiple_items/apple_and_bottle.mp4"
}
```

- one endpoint that can play all the videos available, regardless of the scenario(api/play-all)
- one endpoint that stops the current video that is playing(api/stop)
- one endpoint that can play a specific video or a specific scenario without the json body, path can be put inside the url
- one endpoint that can get the video that is currently playing(api/current)
- one endpoint that gets all the videos but in a random order, so the model doesnt get predictible(api/play-random)

to clone the repository use this command:
```
git clone https://github.com/mihaixuriciuc/Winnow_Intern_Project
```

Then navigate to the folder:

```
cd Winnow_Intern_Project
```

Make sure that you have python installed,create a virtual env:
```
python3 -m venv .venv
```
Activate it using this for Mac or Linux:
```source .venv/bin/python```
or this for windows: 
``` source .venv/bin/python```

Then run the requirements.txt
```
pip install -r requirements.txt

```

Make sure that you have VLC installed, you need to copy the path to it and paste it in the playback/views.py