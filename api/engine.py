import random
import math
from sentence_transformers import SentenceTransformer
import numpy as np

# ==========================================================
# MODELO SEMÂNTICO
# ==========================================================

model = SentenceTransformer("all-MiniLM-L6-v2")

# Âncoras narrativas (não aparecem para o jogador)
ANCHORS = {
    "combate": model.encode("luta batalha ataque violência confronto"),
    "magia": model.encode("feitiço magia energia mística poder arcano"),
    "drama": model.encode("tensão medo silêncio suspense perigo"),
}

# ==========================================================
# ESTADO GLOBAL DAS SALAS
# ==========================================================

ROOMS = {}


def get_room(room_id):
    if room_id not in ROOMS:
        ROOMS[room_id] = {
            "boss_hp": 120,
            "fase": 1,
            "entropia": 0.0
        }
    return ROOMS[room_id]


# ==========================================================
# FUNÇÃO QWAN (influencia o tom)
# ==========================================================

def detectar_tom(texto):
    vetor = model.encode(texto)
    scores = {}

    for chave, anchor in ANCHORS.items():
        sim = np.dot(vetor, anchor) / (
            np.linalg.norm(vetor) * np.linalg.norm(anchor)
        )
        scores[chave] = sim

    dominante = max(scores, key=scores.get)

    if scores[dominante] > 0.55:
        return dominante
    return "neutro"


# ==========================================================
# NARRADOR CINEMATOGRÁFICO
# ==========================================================

def narrar_acao(texto, tom):
    falas = [
        "— Isso termina agora.",
        "— Venha, criatura.",
        "— Pelo destino.",
        "— Não hoje."
    ]

    fala = random.choice(falas)

    if tom == "combate":
        return f"""
O impacto do seu movimento rompe o silêncio do salão.

{fala}

O ar vibra com o peso da decisão.
A criatura reage com um rugido áspero,
mas você já está em movimento.
"""

    elif tom == "magia":
        return f"""
Um brilho sutil percorre o ambiente enquanto sua energia desperta.

{fala}

O ar se dobra ao redor de suas mãos.
Algo invisível responde ao seu chamado.
"""

    elif tom == "drama":
        return f"""
O silêncio antes do golpe é quase ensurdecedor.

{fala}

Seus passos ecoam no chão úmido.
A tensão é tão palpável quanto o cheiro da batalha.
"""

    else:
        return f"""
Você avança.

{fala}

O mundo parece segurar a respiração.
"""


# ==========================================================
# SISTEMA DE COMBATE
# ==========================================================

def rolar_d20():
    return random.randint(1, 20)


def calcular_dano(base=8):
    return random.randint(base - 3, base + 3)


def atualizar_fase(room):
    hp = room["boss_hp"]

    if hp < 40:
        room["fase"] = 3
    elif hp < 80:
        room["fase"] = 2
    else:
        room["fase"] = 1


def narrar_boss(room):
    if room["fase"] == 1:
        return "A criatura mantém postura defensiva, analisando cada movimento."
    elif room["fase"] == 2:
        return "Ferido, o monstro se torna mais agressivo. Seus olhos brilham com fúria."
    else:
        return "Desesperado, o anfíbio ruge e ataca sem cálculo, pura sobrevivência."


# ==========================================================
# CRIAR SESSÃO
# ==========================================================

def criar_sessao(nome, classe, room_id):
    room = get_room(room_id)

    personagem = {
        "nome": nome,
        "classe": classe,
        "hp": 100,
        "mana": 60,
        "xp": 0
    }

    return {
        "session_id": f"{room_id}_{nome}",
        "personagem": personagem
    }


# ==========================================================
# ANALISAR CENA (NARRATIVO PURO)
# ==========================================================

def analisar_qwan_narrativo(textos, room_id="default"):
    texto = textos[0]
    room = get_room(room_id)

    tom = detectar_tom(texto)

    narrativa = narrar_acao(texto, tom)

    return {
        "narrativa": narrativa.strip()
    }


# ==========================================================
# COMBATE ESTRUTURADO
# ==========================================================

def combate(session_id, acao, room_id="default"):
    room = get_room(room_id)

    rolagem = rolar_d20()
    dano = calcular_dano()

    sucesso = rolagem >= 10

    if sucesso:
        room["boss_hp"] -= dano

    atualizar_fase(room)

    descricao_boss = narrar_boss(room)

    if sucesso:
        narrativa = f"""
Você investe contra o inimigo.

O dado rola… {rolagem}.

O golpe acerta com força.
A criatura recua sob o impacto.

{descricao_boss}
"""
    else:
        narrativa = f"""
Você ataca com determinação.

O dado rola… {rolagem}.

A criatura esquiva por pouco.
Seu movimento corta apenas o ar.

{descricao_boss}
"""

    return {
        "narrativa": narrativa.strip(),
        "hp": 100,
        "mana": 60,
        "xp": 10 if sucesso else 0,
        "hp_inimigo": max(room["boss_hp"], 0)
    }
