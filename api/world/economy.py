import random

ITENS = {

"espada":100,
"poção":30,
"armadura":250,
"amuleto":500

}


def preco_dinamico(item, demanda):

    base = ITENS[item]

    return int(base * (1 + demanda*0.5) * random.uniform(0.8,1.2))
