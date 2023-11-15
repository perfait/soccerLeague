from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('leagueStandings')
        
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')


        context = {'form':form}
        return render(request, 'league/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('leagueStandings')

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('leagueStandings')
            
            else:
                messages.info(request, 'Username OR password is incorrect')


        context = {}
        return render(request, 'league/login.html', context)



def logoutUser(request):
    logout(request)

    return redirect('login')



@login_required(login_url='login')
def addTeams(request):
    form = teamForm()
    if request.method == 'POST':
        form = teamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team added successfully!')
        else:
            messages.error(request, 'A team with the same name already exists!')

    context = {'form': form}

    return render(request, 'league/add-teams.html', context)




@login_required(login_url='login')
def addPlayers(request):
    form = playerForm()
    if request.method == 'POST':
        form = playerForm(request.POST)
        if form.is_valid():
            selected_team_id = form.cleaned_data['team'].id
            player = form.save(commit=False)
            player.team_name_id = selected_team_id
            player.save()

            messages.success(request, 'Player added successfully!')
            #return HttpResponse("Player added successfully")
        
        else:
            messages.error(request, 'Player added successfully!')
            #return HttpResponse("Invalid form")
        
        
    context = {'form': form}
    return render(request, 'league/add-players.html', context)




def topScorers(request):
    top_scorers = Player.objects.select_related('team_name').order_by('-goals', 'player_name')[:10]
    context = {'top_scorers': top_scorers}
    return render(request, 'league/top-scorers.html', context)




def leagueStandings(request):
    standings = Team.objects.all().order_by('-points', '-goal_difference', '-goals_for', 'team_name')
    context = {'standings': standings}
    return render(request, 'league/league-standings.html', context)


@login_required(login_url='login')
def updateScores(request):
    update_scores_form = UpdateScoresForm()
    if request.method == 'POST':
        update_scores_form = UpdateScoresForm(request.POST)

        if update_scores_form.is_valid():
            home_team = update_scores_form.cleaned_data['home_team']
            home_team_score = update_scores_form.cleaned_data['home_team_score']
            away_team = update_scores_form.cleaned_data['away_team']
            away_team_score = update_scores_form.cleaned_data['away_team_score']


            # Calculate the match result (W: Win, L: Loss, D: Draw)
            if home_team_score > away_team_score:
                home_team_result = 'W'
                away_team_result = 'L'
            elif home_team_score < away_team_score:
                home_team_result = 'L'
                away_team_result = 'W'
            else:
                home_team_result = 'D'
                away_team_result = 'D'

            # Update the home team's stats 
            home_team.matches_played += 1
            home_team.won += (home_team_result == 'W')
            home_team.lost += (home_team_result == 'L')
            home_team.drawn += (home_team_result == 'D')
            home_team.goals_for += home_team_score
            home_team.goals_against += away_team_score
            home_team.goal_difference += home_team_score - away_team_score
            home_team.points += 3 if home_team_result == 'W' else 1 if home_team_result == 'D' else 0
            home_team.last_match = home_team_result
            


            # Update the away team's stats
            away_team.matches_played += 1
            away_team.won += (away_team_result == 'W')
            away_team.lost += (away_team_result == 'L')
            away_team.drawn += (away_team_result == 'D')
            away_team.goals_for += away_team_score
            away_team.goals_against += home_team_score
            away_team.goal_difference += away_team_score - home_team_score
            away_team.points += 3 if away_team_result == 'W' else 1 if away_team_result == 'D' else 0
            away_team.last_match = away_team_result

            # Save the updated statistics to the database
            home_team.save()
            away_team.save()
            
            messages.success(request, 'Scores updated successfully!')
            #return HttpResponse("Scores updated successfully")
        else:  
            messages.error(request, 'Home Team and Away Team cannot be the same.')
            #return HttpResponse("Home Team and Away Team cannot be the same.")

    return render(request, 'league/update-scores.html', {'update_scores_form': update_scores_form})




@login_required(login_url='login')
def addScorers(request):
    add_scorer_form = AddScorerForm()

    if request.method == 'POST':
        add_scorer_form = AddScorerForm(request.POST)
        if add_scorer_form.is_valid():
            scorer_name = add_scorer_form.cleaned_data['scorer_name']
            goals_scored = add_scorer_form.cleaned_data['goals_scored']
            # Check if the scorer already exists in the database
            if Player.objects.filter(player_name=scorer_name).exists():
                # Update the scorer's goals scored
                scorer = Player.objects.get(player_name=scorer_name)
                scorer.goals += goals_scored
                scorer.save()
                messages.success(request, 'Scorer added successfully!')
            else:
                messages.error(request, 'Player does not exist!')

            

    return render(request, 'league/add-scorers.html', {'add_scorer_form': add_scorer_form})



def player_names_autosuggest(request):
    search_term = request.GET.get('search', '')

    players = Player.objects.filter(player_name__istartswith=search_term).values('player_name')

    return JsonResponse(list(players), safe=False)
