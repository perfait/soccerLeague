from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class teamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['team_name']

    def clean_team_name(self):
        team_name = self.cleaned_data.get('team_name')
        if Team.objects.filter(team_name=team_name).exists():
            raise forms.ValidationError("Invalid entry!")
        return team_name


class playerForm(forms.ModelForm):
    player_name = forms.CharField(label='Player Name')
    team = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label="Select a Team")

    class Meta:
        model = Player
        fields = ['player_name', 'team']


class UpdateScoresForm(forms.Form):
    home_team = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label="Select a Home Team")
    home_team_score = forms.IntegerField()
    away_team = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label="Select an Away Team")
    away_team_score = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        home_team = cleaned_data.get("home_team")
        away_team = cleaned_data.get("away_team")

        # Check if the home and away teams are the same
        if home_team == away_team:
            raise forms.ValidationError("Invalid entry")
        


class AddScorerForm(forms.Form):
    scorer_name = forms.CharField(max_length=255)
    goals_scored = forms.IntegerField()