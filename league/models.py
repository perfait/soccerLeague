from django.db import models

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=255)
    matches_played = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    drawn = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    goal_difference = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    last_match = models.CharField(max_length=10, default="None")

    def __str__(self):
        return self.team_name


class Player(models.Model):
    player_name = models.CharField(max_length=255)
    team_name = models.ForeignKey(Team, on_delete=models.CASCADE)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)

    def __str__(self):
        return self.player_name   
