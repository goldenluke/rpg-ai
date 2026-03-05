# api/multiplayer/rooms.py

ROOMS = {}


def get_room(room_id):

    if room_id not in ROOMS:

        ROOMS[room_id] = {

            "players": {},
            "history": []

        }

    return ROOMS[room_id]


def add_player(room_id, player_id, player_name):

    room = get_room(room_id)

    if player_id not in room["players"]:

        room["players"][player_id] = {

            "id": player_id,
            "name": player_name,

            "hp": 100,
            "mana": 60,
            "xp": 0,

            "inventario": ["Espada", "Poção"],

            "position": {
                "x": 0,
                "y": 0
            }

        }


def get_player(room_id, player_id):

    room = get_room(room_id)

    return room["players"].get(player_id)


def update_player(room_id, player_id, data):

    player = get_player(room_id, player_id)

    if not player:
        return

    player.update(data)


def move_player(room_id, player_id, dx, dy):

    player = get_player(room_id, player_id)

    if not player:
        return

    player["position"]["x"] += dx
    player["position"]["y"] += dy

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


def add_event(room_id, event):

    room = get_room(room_id)

    room["history"].append(event)

    if len(room["history"]) > 100:
        room["history"] = room["history"][-100:]


