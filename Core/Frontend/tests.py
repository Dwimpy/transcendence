# yourapp/tests.py
import json
import threading
import websocket
from channels.layers import get_channel_layer
from channels.testing import ChannelsLiveServerTestCase
from django.contrib.auth import get_user_model
from Frontend.model.ponglobby import PongLobby

User = get_user_model()


class RoomCreationTest(ChannelsLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create a user for testing
        cls.user = User.objects.create(username='testuser', password='testpassword')

    def test_create_new_room_and_broadcast(self):
        channel_layer = get_channel_layer()

        # Connect to the WebSocket
        ws = websocket.WebSocket()
        ws.connect(f"ws{self.live_server_url[4:]}lobby/")  # Adjust the URL based on your routing

        # Create a new room
        room_data = {'name': 'Test Room', 'player_count': 1, 'is_room_full': False}
        PongLobby.create_room()

        # Wait for a short moment to allow for asynchronous processing
        threading.Event().wait(0.1)

        # Receive message from WebSocket
        response = json.loads(ws.recv())

        # Assert that the expected message was received
        self.assertEqual(response['type'], 'new_room')
        self.assertEqual(response['room_data'], room_data)

        # Clean up
        ws.close()
