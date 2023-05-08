import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Gamer, Event, Gametype, Game
from rest_framework.authtoken.models import Token

class EventTests(APITestCase):
    # fixtures
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events']

    def setUp(self):
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_event(self):
        url = "/events"
        data = {
            "description": "this is my test description",
            "date": "2023-06-01",
            "time": "16:00:00",
            "game": 1
        }
        organizer = Gamer.objects.first()
        game = Game.objects.get(pk=data['game'])
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response['description'], "this is my test description")
        self.assertEqual(json_response['date'], "2023-06-01")
        self.assertEqual(json_response['time'], "16:00:00")
        self.assertEqual(json_response['game'], game.id)

    def test_get_event(self):
        event = Event()
        event.description = "this is my test description"
        event.date = "2023-06-01"
        event.time = "16:00:00"
        event.game_id = Game.objects.first().id
        event.organizer_id = Gamer.objects.first().id
        event.save()
        event.attendees.set([])

        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)
        # print(json.loads(organizer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['description'], "this is my test description")
        self.assertEqual(json_response['date'], "2023-06-01")
        self.assertEqual(json_response['time'], "16:00:00")
        self.assertEqual(json_response['game'], 1)
        # self.assertEqual(json_response['organizer'], organizer)
        self.assertEqual(json_response['attendees'], [])

    def test_put_event(self):
        event = Event()
        event.description = "this is my test description"
        event.date = "2023-06-01"
        event.time = "16:00:00"
        event.game_id = Game.objects.first().id
        event.organizer_id = Gamer.objects.first().id
        event.save()
        event.attendees.set([])

        data = {
            "description": "this is my update description",
            "date": "2023-07-01",
            "time": "10:00:00",
            "game": 1
        }

        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['description'], "this is my update description")
        self.assertEqual(json_response['date'], "2023-07-01")
        self.assertEqual(json_response['time'], "10:00:00")
        self.assertEqual(json_response['game'], 1)
        self.assertEqual(json_response['attendees'], [])

    def test_delete_event(self):
        event = Event()
        event.description = "this is my test description"
        event.date = "2023-06-01"
        event.time = "16:00:00"
        event.game_id = Game.objects.first().id
        event.organizer_id = Gamer.objects.first().id
        event.save()
        event.attendees.set([])
        event.save()
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)