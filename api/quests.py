from sentence_transformers import SentenceTransformer
import numpy as np
import random

model = SentenceTransformer("all-MiniLM-L6-v2")


QUEST_TEMPLATES = [
    "Derrote a criatura que habita {lugar}",
    "Recupere o artefato perdido em {lugar}",
    "Investigue os ruídos vindos de {lugar}",
    "Proteja o viajante que atravessa {lugar}"
]


LUGARES = [
    "a câmara antiga",
    "as catacumbas",
    "o templo abandonado",
    "a floresta escura"
]


def gerar_quest(contexto):

    emb_context = model.encode(contexto)

    template = random.choice(QUEST_TEMPLATES)
    lugar = random.choice(LUGARES)

    quest = template.format(lugar=lugar)

    return {
        "quest": quest,
        "contexto": contexto
    }
