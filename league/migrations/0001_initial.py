# Generated by Django 4.2.6 on 2023-10-21 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=255)),
                ('matches_played', models.IntegerField(default=0)),
                ('won', models.IntegerField(default=0)),
                ('drawn', models.IntegerField(default=0)),
                ('lost', models.IntegerField(default=0)),
                ('goals_for', models.IntegerField(default=0)),
                ('goals_against', models.IntegerField(default=0)),
                ('goal_difference', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('last_match', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_name', models.CharField(max_length=255)),
                ('goals', models.IntegerField(default=0)),
                ('assists', models.IntegerField(default=0)),
                ('team_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.team')),
            ],
        ),
    ]
