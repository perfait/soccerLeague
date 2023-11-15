from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.leagueStandings, name='leagueStandings'),
    path('top-scorers/', views.topScorers, name='topScorers'),
    path('add-teams', views.addTeams, name='addTeams'),
    path('add-players', views.addPlayers, name='addPlayers'),
    path('update-scores', views.updateScores, name='updateScores'),
    path('add-scorers', views.addScorers, name='addScorers'),
    path('api/players/', views.player_names_autosuggest, name='player_names_autosuggest'),
    
]
