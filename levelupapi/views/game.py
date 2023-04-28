from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, Gametype


class GameView(ViewSet):
    """game view"""

    def retrieve(self, request, pk=None):
        """handle GET requests for single game"""
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request):
        """handle GET requests for all games"""
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """handle POST request for games"""
        print(request.data)
        gamer = Gamer.objects.get(user=request.auth.user)
        game_type = Gametype.objects.get(pk=request.data['game_type'])
        game = Game.objects.create(
            title=request.data['title'],
            maker=request.data['maker'],
            number_of_players=request.data['number_of_players'],
            skill_level=request.data['skill_level'],
            gamer=gamer,
            type=game_type
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)


class GameSerializer(serializers.ModelSerializer):
    """serializer for gameview"""
    class Meta:
        model = Game
        fields = ('id', 'title', 'number_of_players', 'maker', 'skill_level', 'type', 'gamer')
