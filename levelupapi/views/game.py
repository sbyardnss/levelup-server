from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, Gametype
from django.db.models import Count, Q
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import permissions
from levelupapi.permission import UserCreatedGameOrDelete
class GameView(ViewSet):
    """game view"""
    permission_classes = [ UserCreatedGameOrDelete ]
    queryset = Game.objects.none()
    def retrieve(self, request, pk=None):
        """handle GET requests for single game"""
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """handle GET requests for all games"""
        # games = Game.objects.all()
        # why does the code below use the games variable name again?
        gamer = Gamer.objects.get(user=request.auth.user)
        games = Game.objects.annotate(event_count=Count('events'), user_event_count=Count('events', filter=Q(events__organizer=gamer)))
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(type=game_type)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    # OLD CREATE BEFORE VALIDATION SERIALIZER
    # def create(self, request):
    #     """handle POST request for games"""
    #     print(request.data)
    #     gamer = Gamer.objects.get(user=request.auth.user)
    #     game_type = Gametype.objects.get(pk=request.data['game_type'])
    #     game = Game.objects.create(
    #         title=request.data['title'],
    #         maker=request.data['maker'],
    #         number_of_players=request.data['number_of_players'],
    #         skill_level=request.data['skill_level'],
    #         gamer=gamer,
    #         type=game_type
    #     )
    #     serializer = GameSerializer(game)
    #     return Response(serializer.data)

    def create(self, request):
        """handle POST request for gamers"""
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request, pk):
        """handle PUT requests for games"""
        game = Game.objects.get(pk=pk)
        game.title = request.data['title']
        game.maker = request.data['maker']
        game.number_of_players = request.data['number_of_players']
        game.skill_level = request.data['skill_level']

        game_type = Gametype.objects.get(pk=request.data['type'])
        game.type = game_type
        self.check_object_permissions(request, game)
        game.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """handle DELETE requests for games"""
        game = Game.objects.get(pk=pk)
        self.check_object_permissions(request, game)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CreateGameSerializer(serializers. ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'maker', 'number_of_players', 'skill_level', 'type']

class GameSerializer(serializers.ModelSerializer):
    """serializer for gameview"""
    event_count = serializers.IntegerField(default=None)
    user_event_count = serializers.IntegerField(default=None)
    class Meta:
        model = Game
        fields = ('id', 'title', 'number_of_players', 'maker', 'skill_level', 'type', 'gamer', 'event_count', 'user_event_count')
        depth = 1
