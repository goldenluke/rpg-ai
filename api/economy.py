import random

ITENS = {

    "espada": 100,
    "poção": 30,
    "armadura": 250,
    "amuleto": 500

}


def preco_dinamico(item, entropia):

    base = ITENS[item]

    var = random.uniform(0.7, 1.3)

    caos = 1 + (entropia * 0.5)

    return int(base * var * caos)


def gerar_loja(entropia):

    itens = random.sample(list(ITENS.keys()), 3)

    loja = {}

    for i in itens:
        loja[i] = preco_dinamico(i, entropia)

    return loja
