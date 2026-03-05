# api/world/dungeons.py

import random
import uuid
from typing import Dict, Any, List

from .monsters import generate_monster


ROOM_TYPES = [
    "inimigo",
    "tesouro",
    "vazio",
    "armadilha"
]


TREASURES = [
    "ouro",
    "poção",
    "espada antiga",
    "amuleto mágico"
]


def generate_room() -> Dict[str, Any]:
    """
    Gera uma sala procedural.
    """
    room_type = random.choice(ROOM_TYPES)

    room = {
        "tipo": room_type
    }

    if room_type == "inimigo":
        room["monstro"] = generate_monster("goblin")

    if room_type == "tesouro":
        room["item"] = random.choice(TREASURES)

    if room_type == "armadilha":
        room["dano"] = random.randint(5, 20)

    return room


def generate_dungeon() -> Dict[str, Any]:
    """
    Gera dungeon completa.
    """
    dungeon_id = str(uuid.uuid4())

    rooms: List[Dict[str, Any]] = []

    room_count = random.randint(5, 12)

    for _ in range(room_count):
        rooms.append(generate_room())

    return {
        "id": dungeon_id,
        "salas": rooms,
        "boss": generate_monster("orc")
    }


def explore_room(room: Dict[str, Any]) -> Dict[str, Any]:
    """
    Resolve evento ao entrar em sala.
    """
    result = {"evento": room["tipo"]}

    if room["tipo"] == "inimigo":
        result["combate"] = room["monstro"]

    if room["tipo"] == "tesouro":
        result["loot"] = room["item"]

    if room["tipo"] == "armadilha":
        result["dano"] = room["dano"]

    return result
