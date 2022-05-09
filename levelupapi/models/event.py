from django.db import models

from levelupapi.models.gamer import Gamer

class Event(models.Model):

    game = models.ForeignKey("game",on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey("gamer", on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Gamer, related_name="gamers")