# api/world/history_store.py

WORLD_HISTORY = []


def add_history(event):

    WORLD_HISTORY.append(event)

    # limitar tamanho
    if len(WORLD_HISTORY) > 200:
        WORLD_HISTORY.pop(0)


def get_history():

    return WORLD_HISTORY
