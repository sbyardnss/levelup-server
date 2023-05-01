from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game
from rest_framework.decorators import action
from django.db.models import Count, Q

class EventView(ViewSet):
    """level up event view"""

    def retrieve(self, request, pk=None):
        """handle GET request for individual event"""
        try:
            event = Event.objects.annotate(attendee_count=Count("attendees")).get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """handle GET request for all events"""
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.annotate(attendee_count=Count("attendees"), joined=Count('attendees', filter=Q(attendees=gamer)))
        # print(request.query_params['game'])
        if "game" in request.query_params:
            events = events.filter(game=request.query_params['game'])
        # Set the `joined` property on every event
        # for event in events:
        #     gamer = Gamer.objects.get(user=request.auth.user)
        #     # Check to see if the gamer is in the attendees list on the event
        #     event.joined = gamer in event.attendees.all()
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
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def update(self, request, pk):
        """handle PUT requests for events"""
        print(request.data)
        event = Event.objects.get(pk=pk)
        event.description = request.data['description']
        event.date = request.data['date']
        event.time = request.data['time']

        game = Game.objects.get(pk=request.data['game'])
        event.game = game
        event.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """handle DELETE requests for events"""
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """delete request for user to leave attendees"""
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)


class GamerSerializer(serializers.ModelSerializer):
    """serializer for gamer property on events"""
    class Meta:
        model = Gamer
        fields = ('id', 'full_name')


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for eventview"""
    organizer = GamerSerializer(many=False)
    attendee_count = serializers.IntegerField(default=None)
    class Meta:
        model = Event
        fields = ('id', 'description', 'date', 'time',
                  'organizer', 'attendees', 'game', 'joined', 'attendee_count')
        depth = 2


