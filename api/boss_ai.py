def boss_strategy(room):

    entropia = room.get("entropia", 0)

    if entropia < 0.3:
        return "defensivo"

    if entropia < 0.6:
        return "agressivo"

    return "caótico"
