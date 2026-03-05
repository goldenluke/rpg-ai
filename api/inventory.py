import random

ITEMS = [
    ("Espada antiga", "arma"),
    ("Poção de cura", "consumível"),
    ("Amuleto estranho", "artefato"),
    ("Pergaminho arcano", "magia"),
    ("Adaga enferrujada", "arma")
]


def gerar_item(entropia):

    base = random.choice(ITEMS)

    raridade_roll = random.random()

    if raridade_roll > 0.95:
        raridade = "lendário"

    elif raridade_roll > 0.8:
        raridade = "raro"

    else:
        raridade = "comum"

    return {
        "nome": base[0],
        "tipo": base[1],
        "raridade": raridade
    }
