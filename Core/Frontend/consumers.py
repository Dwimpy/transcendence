import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.accept()

	async def disconnect(self, close_code):
		pass

	async def receive(self, text_data=None, bytes_data=None):
		data = json.loads(text_data)
		message = data['message']
		if 'what the fuk' in message:
			print("HELLO WORLDDDD")
		await self.send(text_data=json.dumps({'message': 'Test websocket'}))
