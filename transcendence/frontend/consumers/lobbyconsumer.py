import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from ..models.customuser import CustomUser
from ..models.lobby import Lobby


class LobbyConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        print("CONNECTEd")
        self.group_name = None

    async def connect(self):
        self.group_name = "group_lobby"
        await self.accept()
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        data = json.loads(text_data)
        command = data.get('new_room')
        user = await CustomUser.get_user_by_username('andrei')
        lobby = await Lobby.get_or_create_lobby()
        if command == 'new_room':
            room = await lobby.create_room('another_room', user)
            if room is not None:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "broadcast_new_room",
                        "room_data": {
                            "room_name": room.get_name(),
                            "users": [user.to_dict() for user in await room.get_users()],
                            "player_count": room.player_count,
                            "is_full": room.is_room_full
                        },
                    }
                )
            else:
                async for room in lobby.rooms.all():
                    print(room)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "broadcast_room_exists"
                    }
                )
        else:
            pass

    async def broadcast_new_room(self, event):
        room_data = event['room_data']
        print(room_data)
        await self.send(text_data=json.dumps({
            'room:': room_data
        }))

    async def broadcast_room_exists(self, event):
        await self.send(text_data=json.dumps({
            'message': 'Room already exists '
        }))
