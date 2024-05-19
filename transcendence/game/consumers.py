# pong/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class Bar:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.speed = speed

    def go_up(self):
        self.y_speed = -self.speed

    def go_down(self):
        self.y_speed = self.speed

    def stop(self):
        self.y_speed = 0
        self.x_speed = 0

    def get_speed_x(self):
        return self.x_speed

    def get_speed_y(self):
        return self.y_speed




class PongConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = 'pong_room'
        self.room_group_name = 'pong_group'
        self.ball_x = 0
        self.ball_y = 0
        self.ball_x_speed = 0
        self.ball_y_speed = 0

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get('type')
        speed = 400
        if event_type == 'mouse_move':
            x = data.get('x')
            y = data.get('y')
            print(f"Mouse move to ({x}, {y})")
        elif event_type == 'key_down':
            key = data.get('key')
            if key == 'ArrowUp':
                self.ball_y_speed = -speed
            if key == 'ArrowDown':
                self.ball_y_speed = speed
            if key == 'ArrowLeft':
                self.ball_x_speed = -speed
            if key == 'ArrowRight':
                self.ball_x_speed = speed

        elif event_type == 'key_up':
            key = data.get('key')
            if key == 'ArrowUp' or key == 'ArrowDown':
                self.ball_y_speed = 0
            if key == 'ArrowLeft' or key == 'ArrowRight':
                self.ball_x_speed = 0
        self.ball_x += self.ball_x_speed
        self.ball_y += self.ball_y_speed
        print(f"Key pressed: {data}")

        # Send circle position to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'circle_position',
                'circle_x': self.ball_x,  # Add circle position data here
                'circle_y': self.ball_y,
                'circle_x_speed': self.ball_x_speed,
                'circle_y_speed': self.ball_y_speed
            }
        )

    async def pong_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def circle_position(self, event):
        # Handle circle position message
        circle_x = event['circle_x']
        circle_y = event['circle_y']
        print(f"Circle position: ({circle_x}, {circle_y})")
        # Send circle position to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_circle_position',
                'circle_x': circle_x,
                'circle_y': circle_y,
                'circle_x_speed': self.ball_x_speed,
                'circle_y_speed': self.ball_y_speed
            }
        )

    async def send_circle_position(self, event):
        # Send circle position message to the frontend
        await self.send(text_data=json.dumps({
            'type': 'circle_position',
            'circle_x': event['circle_x'],
            'circle_y': event['circle_y'],
            'circle_x_speed': self.ball_x_speed,
            'circle_y_speed': self.ball_y_speed
        }))
