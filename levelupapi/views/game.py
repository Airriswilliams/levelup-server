"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game
from levelupapi.models.game_type import GameType
from levelupapi.models.gamer import Gamer
from django.core.exceptions import ValidationError


class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game 

        Returns:
            Response -- JSON serialized game 
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
# the "request" from the method parameters holds all the information for the request from the client.
# The "request.query_params" is a dictionary of any query parameters that were in the url. Using the .get method
# on a dictionary is a safe way to find if a key is present on the dictionary. If the "type" key is not present
# on the dictionary it will return "None" 

# the game_type variable is now a list of Game objects. adding many=true lets the serializer know
# that a list vs. a single object is to be serialized.
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    # this will replace the previous create method
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
# similar to retrieve, we grab the "Game" obj we want from the db, then the next lines are setting
# the fields on "game" to the values coming from the client, like in the "create" method. After all 
# fields are set, the changes are saved to the db.

        game = Game.objects.get(pk=pk)
        serializer = CreateGameSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


    
    
    # def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized game instance
        """
        # get the game that is logged in. All postman & fetch requests have the user's auth token in the headers,
        # the request will get the user object based on that token. Next we use "request.auth.user" to get the
        # "Gamer" object based on the user.
        # gamer = Gamer.objects.get(user=request.auth.user)
        # retrieve the "GameType" obj from the database. We do this to make sure the game type the user is trying to add
        # the new game actually exists in the database. The data passed in from the client is held in the request.data dict
        # Whichever keys are used on the request.data must match what the client is passing over to the server.
        # game_type = GameType.objects.get(pk=request.data["game_type"])

        # game = Game.objects.create(
        #     title=request.data["title"],
        #     maker=request.data["maker"],
        #     number_of_players=request.data["number_of_players"],
        #     skill_level=request.data["skill_level"],
        #     gamer=gamer,
        #     game_type=game_type
        # )
        # serializer = GameSerializer(game)
        # return Response(serializer.data)
    # After the "create" has finished the "game" variable is now the new game instance, including the new id.
    # The object can be serialized and returned to the client now just like in the "retrieve" method
    
 

        
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:
        model = Game
        fields = ('id', 'game_type','title', 'maker', 'gamer', 'number_of_players', 'skill_level')
        depth = 1
# the Meta class holds the configuration for the serializer. We're telling the serializer to use the "Game" 
# model and to include the 'id', 'game_type','title', 'maker', 'gamer', 'number_of_players', 'skill_level' fields

class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'game_type', 'title', 'maker', 'number_of_players', 'skill_level']
        # fields = (__all__)