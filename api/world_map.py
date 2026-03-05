import random

BIOMAS = [
    "floresta",
    "montanhas",
    "deserto",
    "pântano"
]


def gerar_tile(x, y):

    seed = x * 928371 + y * 123721
    random.seed(seed)

    bioma = random.choice(BIOMAS)

    perigo = random.randint(1, 5)

    return {
        "x": x,
        "y": y,
        "bioma": bioma,
        "perigo": perigo
    }
