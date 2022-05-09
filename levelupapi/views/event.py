"""View module for handling requests about events"""
from ast import Try
import re
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game
from levelupapi.models import gamer
from levelupapi.models.gamer import Gamer
from django.core.exceptions import ValidationError
from rest_framework.decorators import action



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
        gamer = Gamer.objects.get(user=request.auth.user)
        # instance of a gamer object, checking if the gamer apart of this event or not?

        
        game = request.query_params.get('game', None)
        if game is not None:
            events = events.filter(game_id=game)
        
        for event in events:
            event.joined = gamer in event.attendees.all()
        # "all" method gets every gamer attending the event. The conditional,"gamer in event"
        # "event.attendees.all()" will evaluate to True or False if the gamer is in the atendees list
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
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    # Using the "action" decorator turns a method into a new route. The action will accept "POST" methods
    # and b/c "detail=TRUE" the url will include the pk. We need the pk so we will know which event the user
    # wants to sign up for.
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)

        
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'description','date', 'time', 'organizer','attendees','joined')
        depth = 2
# the Meta class holds the configuration for the serializer. We're telling the serializer to use the "Event" 
# model and to include the "id", game, description, date, time and organizer fields
# depth gives the nested user data

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'game', 'description','date', 'time', 'organizer')
        # fields = (__all__)

    
    