from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Gametype

class GameTypeView(ViewSet):
    """Level up game types view"""
    def retrieve(self, request, pk=None):
        """handle GET request or individual gametype"""
        game_type = Gametype.objects.get(pk=pk)
        serializer = GameTypeSerializer(game_type)
        return Response(serializer.data)

    def list(self, request):
        """handles GET request for all gametypes"""
        game_types = Gametype.objects.all()
        serializer = GameTypeSerializer(game_types, many=True)
        return Response(serializer.data)



class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for gametype views"""
    class Meta:
        model = Gametype
        fields = ('id', 'label')
