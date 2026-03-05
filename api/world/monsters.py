# api/world/monsters.py

import random
import uuid
from typing import Dict, Any


MONSTERS = {
    "goblin": {
        "hp": 30,
        "ataque": 5,
        "xp": 10
    },
    "orc": {
        "hp": 60,
        "ataque": 10,
        "xp": 20
    },
    "troll": {
        "hp": 120,
        "ataque": 18,
        "xp": 50
    },
    "dragao": {
        "hp": 300,
        "ataque": 40,
        "xp": 200
    }
}


BIOME_MONSTERS = {
    "floresta": ["goblin", "orc"],
    "montanhas": ["orc", "troll"],
    "deserto": ["goblin"],
    "pântano": ["goblin", "troll"]
}


def generate_monster(tipo: str) -> Dict[str, Any]:
    """
    Gera instância de monstro.
    """
    base = MONSTERS[tipo]

    return {
        "id": str(uuid.uuid4()),
        "tipo": tipo,
        "hp": base["hp"],
        "ataque": base["ataque"],
        "xp": base["xp"]
    }


def spawn_monster_for_biome(biome: str) -> Dict[str, Any]:
    """
    Escolhe monstro baseado no bioma.
    """
    choices = BIOME_MONSTERS.get(biome, ["goblin"])

    monster_type = random.choice(choices)

    return generate_monster(monster_type)
