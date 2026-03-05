import random
from collections import deque

PERSONALIDADES = [

    "mercador ganancioso",
    "sábio misterioso",
    "aventureiro aposentado",
    "sacerdote devoto",
    "trapaceiro"

]

NPC_MEMORY = {}

MAX_MEMORY = 10


def get_memory(npc_id):

    if npc_id not in NPC_MEMORY:
        NPC_MEMORY[npc_id] = deque(maxlen=MAX_MEMORY)

    return NPC_MEMORY[npc_id]


def remember(npc_id, texto):

    mem = get_memory(npc_id)
    mem.append(texto)


def npc_response(npc_id, texto):

    remember(npc_id, texto)

    mem = get_memory(npc_id)

    respostas = [
        "Interessante...",
        "Já ouvi algo parecido antes.",
        "Isso pode ser perigoso.",
        "Talvez haja uma recompensa nisso."
    ]

    resposta = random.choice(respostas)

    if len(mem) > 2:

        eco = mem[-2]

        resposta += f" Você disse algo semelhante antes: '{eco[:40]}...'"

    return resposta
