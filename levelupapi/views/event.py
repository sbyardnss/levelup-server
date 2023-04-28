from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game

class EventView(ViewSet):
    """level up event view"""
    def retrieve(self, request, pk=None):
        """handle GET request for individual event"""
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def list(self, request):
        """handle GET request for all events"""
        events = Event.objects.all()
        # print(request.query_params['game'])
        if "game" in request.query_params:
            events = events.filter(game = request.query_params['game'])
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    def create(self, request):
        """handle POST request for events"""
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['game'])
        event = Event.objects.create(
            description=request.data['description'],
            date=request.data['date'],
            time=request.data['time'],
            organizer=gamer,
            game=game
        )
        serializer=EventSerializer(event)
        return Response(serializer.data)

    def update(self, request, pk):
        """handle PUT requests for events"""
        print(request.data)
        event = Event.objects.get(pk=pk)
        event.description = request.data['description']
        event.date = request.data['date']
        event.time=request.data['time']
        
        game = Game.objects.get(pk=request.data['game'])
        event.game=game
        event.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



class GamerSerializer(serializers.ModelSerializer):
    """serializer for gamer property on events"""
    class Meta:
        model = Gamer
        fields = ('id', 'full_name')

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for eventview"""
    organizer = GamerSerializer(many=False)
    class Meta:
        model = Event
        fields = ('id', 'description', 'date', 'time', 'organizer', 'attendees' , 'game')