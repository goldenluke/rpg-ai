"""
ENGINE RPG D&D + QWAN + MiniLLM CRIATIVO
"""

import random
import uuid
import numpy as np
from typing import Dict
from sentence_transformers import SentenceTransformer

# ==========================================================
# MINI LLM
# ==========================================================

model = SentenceTransformer("all-MiniLM-L6-v2")

# Vetores âncora
ANCORAS = {
    "combate": model.encode("batalha luta sangue ataque"),
    "magia": model.encode("magia feitiço arcano poder místico"),
    "drama": model.encode("traição tensão medo perda"),
}

# ==========================================================
# SESSÕES
# ==========================================================

SESSOES: Dict[str, Dict] = {}

# ==========================================================
# QWAN
# ==========================================================

def calcular_qwan(texto):

    emb = model.encode(texto)

    scores = {
        k: float(np.dot(emb, v) / (np.linalg.norm(emb) * np.linalg.norm(v)))
        for k, v in ANCORAS.items()
    }

    intensidade = np.linalg.norm(emb)

    if intensidade > 15:
        regime = "épico"
    elif scores["combate"] > 0.6:
        regime = "tenso"
    elif scores["magia"] > 0.6:
        regime = "místico"
    else:
        regime = "calmo"

    return regime, scores

# ==========================================================
# PERSONAGEM
# ==========================================================

def criar_personagem(nome, classe):

    stats = {k: random.randint(8, 16) for k in [
        "forca", "destreza", "constituicao",
        "inteligencia", "sabedoria", "carisma"
    ]}

    mods = {k: (v - 10) // 2 for k, v in stats.items()}

    if classe == "mago":
        hp = 18 + mods["constituicao"]
        mana = 30
    elif classe == "ladino":
        hp = 24 + mods["constituicao"]
        mana = 12
    else:
        hp = 32 + mods["constituicao"]
        mana = 6

    return {
        "nome": nome,
        "classe": classe,
        "stats": stats,
        "mods": mods,
        "hp": hp,
        "hp_max": hp,
        "mana": mana,
        "mana_max": mana,
        "xp": 0
    }

# ==========================================================
# CRIAR SESSÃO
# ==========================================================

def criar_sessao(nome, classe="guerreiro"):

    session_id = str(uuid.uuid4())

    personagem = criar_personagem(nome, classe)

    SESSOES[session_id] = {
        "personagem": personagem,
        "inimigo": {
            "nome": "Líder Anfíbio",
            "hp": 40,
            "defesa": 13
        },
        "regime": "calmo"
    }

    return {
        "session_id": session_id,
        "personagem": personagem
    }

# ==========================================================
# D20
# ==========================================================

def rolar_d20(mod=0):
    roll = random.randint(1, 20)
    return roll, roll + mod

# ==========================================================
# NARRATIVA CRIATIVA
# ==========================================================

def narrar_combate(regime, dano):

    if regime == "épico":
        return f"⚡ O impacto ressoa como um trovão ancestral causando {dano} de dano!"
    elif regime == "tenso":
        return f"⚔️ O golpe atravessa a defesa inimiga causando {dano} de dano."
    elif regime == "místico":
        return f"✨ A energia arcana explode causando {dano} de dano."
    else:
        return f"O ataque causa {dano} de dano."

# ==========================================================
# COMBATE
# ==========================================================

def combate(session_id, acao):

    sessao = SESSOES.get(session_id)
    if not sessao:
        return {"erro": "Sessão inválida"}

    personagem = sessao["personagem"]
    inimigo = sessao["inimigo"]

    narrativa = ""

    if acao.lower() == "atacar":

        roll, total = rolar_d20(personagem["mods"]["forca"])

        if total >= inimigo["defesa"]:
            dano = random.randint(6, 12)
            inimigo["hp"] -= dano
            narrativa += narrar_combate(sessao["regime"], dano)
        else:
            narrativa += "O golpe falha."

    elif acao.lower() == "magia":

        if personagem["mana"] < 5:
            narrativa += "Mana insuficiente."
        else:
            personagem["mana"] -= 5
            dano = random.randint(8, 14)
            inimigo["hp"] -= dano
            narrativa += narrar_combate("místico", dano)

    else:
        narrativa += "Você assume postura defensiva."

    if inimigo["hp"] <= 0:
        narrativa += "\n🏆 O inimigo cai derrotado."
        personagem["xp"] += 25

    return {
        "narrativa": narrativa,
        "hp": personagem["hp"],
        "mana": personagem["mana"],
        "hp_inimigo": inimigo["hp"],
        "xp": personagem["xp"]
    }

# ==========================================================
# ANALISAR CENA COM QWAN
# ==========================================================

def analisar_qwan_narrativo(textos):

    texto = textos[-1] if textos else ""

    regime, scores = calcular_qwan(texto)

    narrativa = f"""
O ambiente reage às suas palavras.

Regime narrativo: {regime.upper()}

Você declara:
"{texto}"

A tensão no ar muda.
"""

    return {
        "cena": {
            "texto": narrativa.strip(),
            "regime": regime,
            "nivel_campanha": 1,
            "escolhas": ["Atacar", "Magia", "Defender"]
        }
    }
