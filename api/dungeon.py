import random

BIOMAS = [
    "caverna",
    "ruínas antigas",
    "floresta subterrânea",
    "templo abandonado",
    "catacumbas esquecidas"
]

SALAS = [
    "um corredor estreito coberto de musgo",
    "uma câmara circular com pilares quebrados",
    "uma sala inundada até os tornozelos",
    "uma galeria de estátuas antigas",
    "um salão com um altar de pedra"
]


def gerar_sala(seed):

    random.seed(seed)

    bioma = random.choice(BIOMAS)
    sala = random.choice(SALAS)

    return {
        "bioma": bioma,
        "descricao": sala
    }


def gerar_dungeon(room_id, depth):

    seed = hash(room_id) + depth

    sala = gerar_sala(seed)

    return {
        "depth": depth,
        "bioma": sala["bioma"],
        "descricao": sala["descricao"]
    }
