import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Gametype, Gamer, Game
from rest_framework.authtoken.models import Token

class GameTests(APITestCase):
    
    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events']
    def setUp(self):
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    
    def test_create_game(self):
        """test for game post request"""
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/games"

        # Define the request body
        data = {
            "type": 1,
            "skill_level": 5,
            "title": "Clue",
            "maker": "Milton Bradley",
            "number_of_players": 6
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response['title'], "Clue")
        self.assertEqual(json_response['maker'], "Milton Bradley")
        self.assertEqual(json_response['skill_level'], 5)
        self.assertEqual(json_response['number_of_players'], 6)

    def test_get_game(self):
        """ensure get works"""
        # seed database with a game
        game = Game()
        game.type_id = 1
        game.skill_level = 5
        game.title = "Monopoly"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        # initiate request and store response
        response = self.client.get(f"/games/{game.id}")
        # parse the json into a response body (python dictionary)
        json_response = json.loads(response.content)
        # assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["title"], "Monopoly")
        self.assertEqual(json_response["maker"], "Milton Bradley")
        self.assertEqual(json_response["skill_level"], 5)
        self.assertEqual(json_response["number_of_players"], 4)

    def test_put_game(self):
        """ensure put method works"""
        game = Game()
        game.type_id = 1
        game.skill_level = 5
        game.title = "Monopoly"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "type": 1,
            "skill_level": 2,
            "title": "Sorry",
            "maker": "Hasbro",
            "number_of_players": 4
        }

        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET game again to verify changes were made
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["title"], "Sorry")
        self.assertEqual(json_response["maker"], "Hasbro")
        self.assertEqual(json_response["skill_level"], 2)
        self.assertEqual(json_response["number_of_players"], 4)

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.type_id = 1
        game.skill_level = 5
        game.title = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        # DELETE the game you just created
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the game again to verify you get a 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)