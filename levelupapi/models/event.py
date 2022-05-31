from django.db import models

from levelupapi.models.gamer import Gamer

class Event(models.Model):

    game = models.ForeignKey("game",on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey("gamer", on_delete=models.CASCADE)
    attendees = models.ManyToManyField("Gamer", related_name="gamers")
    
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
        
# 
# has this user joined this event, each instance of this event, did the user join event
# adding custom property to "Event" model class. The event class list 
    