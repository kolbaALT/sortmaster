from django.urls import path
from . import views

app_name = 'challenges'

urlpatterns = [
    path('', views.challenge_list, name='list'),
    path('<int:challenge_id>/', views.challenge_detail, name='detail'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('minigames/', views.minigames_list, name='minigames'),
    path('minigames/<int:game_id>/play/', views.minigame_play, name='minigame_play'),
    path('api/submit-challenge/', views.submit_challenge, name='submit_challenge'),
    path('api/save-game-result/', views.save_game_result, name='save_game_result'),
]
