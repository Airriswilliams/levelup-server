# Generated by Django 4.0.4 on 2022-05-09 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0002_game_gamer_alter_game_number_of_players_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(related_name='gamers', to='levelupapi.gamer'),
        ),
    ]
