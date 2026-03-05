from .world_state import WORLD


def world_tick():

    for city in WORLD["cities"].values():

        city["populacao"] += 1
