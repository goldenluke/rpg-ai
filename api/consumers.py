# api/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

from api.multiplayer.rooms import (
    get_room,
    add_player,
    add_event,
    move_player
)


class RPGConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]

        self.room_group_name = f"rpg_{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        room = get_room(self.room_id)

        await self.send(text_data=json.dumps({

            "type": "history",
            "data": room["history"]

        }))


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):

        data = json.loads(text_data)

        msg_type = data.get("type")

        player_id = data.get("player_id")
        player_name = data.get("player_name", "anon")

        text = data.get("text", "")

        add_player(self.room_id, player_id, player_name)

        if msg_type == "move":

            dx = data.get("dx", 0)
            dy = data.get("dy", 0)

            move_player(self.room_id, player_id, dx, dy)

            event = {

                "type": "move",
                "player": player_name,
                "dx": dx,
                "dy": dy

            }

        else:

            event = {

                "type": "narrativa",
                "player": player_name,
                "text": text

            }

        add_event(self.room_id, event)

        await self.channel_layer.group_send(

            self.room_group_name,

            {
                "type": "broadcast_message",
                "message": event
            }

        )


    async def broadcast_message(self, event):

        await self.send(text_data=json.dumps(event["message"]))


        players = get_room(self.room_id)["players"]

        await self.channel_layer.group_send(

            self.room_group_name,

            {
                "type": "broadcast_message",
                "message": {

                    "type":"players",
                    "players":players

                }
            }

)
