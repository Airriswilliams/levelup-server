"""View module for handling requests about events"""
from ast import Try
import re
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game
from levelupapi.models.gamer import Gamer
from django.core.exceptions import ValidationError



class EventView(ViewSet):
    # A views job is to handle requests appropriate to the HTTP verb and the resource
    """Level up events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        game = request.query_params.get('game', None)
        if game is not None:
            events = events.filter(game_id=game)
            
        
        # the event variable is now a list of Event objects. adding many=true lets the serializer know
        # that a list vs. a single object is to be serialized.
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    
    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized game instance
        """
      
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])
        

        event = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            organizer=gamer,
            game=game
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)
    # After the "create" has finished the "event" variable is now the new event instance, including the new id.
    # The object can be serialized and returned to the client now just like in the "retrieve" method
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Event.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

    
    
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'description','date', 'time', 'organizer')
        depth = 2
# the Meta class holds the configuration for the serializer. We're telling the serializer to use the "Event" 
# model and to include the "id", game, description, date, time and organizer fields
# depth gives the nested user data

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'game', 'description','date', 'time', 'organizer')
        # fields = (__all__)