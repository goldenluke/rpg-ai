# api/world/map.py

import random

MAP = {}


BIOMES = [
    "floresta",
    "montanha",
    "planicie",
    "pântano"
]


def get_tile(x, y):

    key = f"{x},{y}"

    if key not in MAP:

        MAP[key] = {

            "biome": random.choice(BIOMES),
            "event": random.random()

        }

    return MAP[key]
