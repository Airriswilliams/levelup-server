from django.db import models
# Join Table

class EventGamer(models.Model):

    gamer = models.ForeignKey("gamer",on_delete=models.CASCADE)
    event = models.ForeignKey("event", on_delete=models.CASCADE)