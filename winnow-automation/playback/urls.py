# playback/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('scenarios', views.get_scenarios), # shows scenarios
    path('play', views.play_video), # plays a specific video via json or a specific folder via json
    path('stop', views.stop_video), # stops the current video
    path('play-all', views.play_all), # plays all the videos in order
    path('play/<path:scenario_path>', views.play_specific), #plays a specific video via path specified in the url
    path('current', views.get_current_video),
    path('play-random', views.play_random)

]