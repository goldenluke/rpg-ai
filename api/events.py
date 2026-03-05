import random

EVENTOS = [
    "Uma névoa densa invade o corredor.",
    "Você ouve passos ecoando nas sombras.",
    "O chão treme levemente sob seus pés.",
    "Um objeto antigo brilha em um canto da sala.",
    "Uma criatura observa à distância."
]


def gerar_evento(entropia):
    prob = min(0.2 + entropia, 0.6)

    if random.random() < prob:
        return random.choice(EVENTOS)

    return None
