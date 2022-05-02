from django.db import models

class Game(models.Model):

    game_type = models.ForeignKey("gametype",on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    gamer = models.ForeignKey("gamer",on_delete=models.CASCADE, default=None)
    number_of_players = models.IntegerField(default=None)
    skill_level = models.IntegerField(default=None)