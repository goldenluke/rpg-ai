import random

EVENTOS = [

"um viajante aparece",
"um monstro ataca",
"um comerciante oferece mercadorias",
"uma ruína antiga é descoberta"

]


def gerar_evento():

    return random.choice(EVENTOS)
