"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game


class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game 

        Returns:
            Response -- JSON serialized game 
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)
        

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
        # the game_type variable is now a list of Game objects. adding many=true lets the serializer know
        # that a list vs. a single object is to be serialized.
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:
        model = Game
        fields = ('id', 'game_type','title', 'maker', 'gamer', 'number_of_players', 'skill_level')
# the Meta class holds the configuration for the serializer. We're telling the serializer to use the "Game" 
# model and to include the 'id', 'game_type','title', 'maker', 'gamer', 'number_of_players', 'skill_level' fields