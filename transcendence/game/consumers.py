# pong/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import time


class Bar:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.y_speed = 0
        self.size = 10
        self.speed = speed
        self.width = 2

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

    def update(self, time):
        self.y += self.y_speed * time
        if self.y < 0:
            self.y = 0
        if self.y + self.size > 100:
            self.y = 100 - self.size


class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_speed = 0
        self.y_speed = 0
        self.size = 5

    def move(self, time):
        self.x += self.x_speed * time
        self.y += self.y_speed * time
        if self.y - self.size < 0:
            self.y_speed *= -1
            self.y = self.size
        if self.y + self.size > 100:
            self.y_speed *= -1
            self.y = 100 - self.size


class HuiGame:
    def __init__(self):
        self.left_bar = Bar(10, 0, 30)
        self.right_bar = Bar(80, 0, 30)
        self.ball = Ball()
        self.ball.x = 30
        self.ball.y = 30
        self.ball.y_speed = -50
        self.ball.x_speed = -50
        self.user1 = ''
        self.user2 = ''
        self.last_update = time.time()
        self.score_left = 0
        self.score_right = 0
        self.max_score = 10
        self.running = True

    def receive_command(self, data, user):
        if user == self.user1:
            event_type = data.get('type')
            if event_type == 'key_down':
                key = data.get('key')
                if key == 'ArrowUp':
                    self.left_bar.go_up()
                if key == 'ArrowDown':
                    self.left_bar.go_down()
            if event_type == 'key_up':
                self.left_bar.stop()

        if user == self.user2:
            event_type = data.get('type')
            if event_type == 'key_down':
                key = data.get('key')
                if key == 'ArrowUp':
                    self.right_bar.go_up()
                if key == 'ArrowDown':
                    self.right_bar.go_down()
            if event_type == 'key_up':
                self.right_bar.stop()
        print(self.left_bar.x, self.left_bar.y)
        print(user, " hui ", self.user1, " hui ", self.user2)

    def bounce_of_left(self):
        within_vertical_range = (self.ball.y + self.ball.size >= self.left_bar.y) and (
                    self.ball.y - self.ball.size <= self.left_bar.y + self.left_bar.size)
        touching_right_side = self.ball.x - self.ball.size / 2 <= self.left_bar.x + self.left_bar.width and self.ball.x >= self.left_bar.x + self.left_bar.width
        return within_vertical_range and touching_right_side

    def bounce_of_right(self):
        within_vertical_range = (self.ball.y + self.ball.size >= self.right_bar.y) and (self.ball.y - self.ball.size <= self.right_bar.y + self.right_bar.size)
        touching_left_side = self.ball.x + self.ball.size / 2 >= self.right_bar.x and self.ball.x <= self.right_bar.x
        return within_vertical_range and touching_left_side

    def run(self):
        if self.running:
            cur_time = time.time()
            self.left_bar.update(cur_time - self.last_update)
            self.right_bar.update(cur_time - self.last_update)
            self.ball.move(cur_time - self.last_update)
            if self.bounce_of_left():
                self.ball.x_speed *= -1
                self.ball.x = self.left_bar.x + self.left_bar.width + self.ball.size / 2
            if self.bounce_of_right():
                self.ball.x_speed *= -1
                self.ball.x = self.right_bar.x - self.ball.size / 2

            if self.ball.x > 100:
                self.ball.x_speed *= -1
                self.ball.x = 50
                self.ball.y = 50
                self.score_left += 1
                if self.score_left > self.max_score:
                    self.running = False
            if self.ball.x < 0:
                self.ball.x_speed *= -1
                self.ball.x = 50
                self.ball.y = 50
                self.score_right += 1

                if self.score_right > self.max_score:
                    self.running = False
            self.last_update = cur_time

    def return_command(self):
        return {
            'type': 'game',
            'circle_x': self.ball.x,  # Add circle position data here
            'circle_y': self.ball.y,
            'left_bar_x': self.left_bar.x,
            'left_bar_y': self.left_bar.y,
            'right_bar_x': self.right_bar.x,
            'right_bar_y': self.right_bar.y,
            'score_left': self.score_left,
            'score_right': self.score_right,

        }
    def restart(self):
        self.score_right = 0
        self.score_left = 0
        self.running = True


class HuiGameasd:

    def __init__(self):
        pass


ggame = HuiGame()


class PongConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = 'pong_room'
        self.room_group_name = 'pong_group'
        self.gamehui = ggame

        if self.gamehui.user1 == '':
            self.gamehui.user1 = self.scope["user"]
        elif self.gamehui.user2 == '' and self.gamehui.user1 != self.scope["user"]:
            self.gamehui.user2 = self.scope["user"]

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
        # print(self.scope["user"])
        data = json.loads(text_data)
        user = self.scope["user"]
        print(user, data, time.time())
        event_type = data.get('type')
        speed = 10
        self.gamehui.receive_command(data, user)
        if (event_type == "update"):
            self.gamehui.run()
        # print(f"Key pressed: {data}")

        # Send circle position to the group
        await self.send(text_data=json.dumps(
            self.gamehui.return_command()
        ))

    async def pong_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))



    async def game(self, hui):
        pass
