import random
import numpy as np

from sentence_transformers import SentenceTransformer

from .memory import remember, recall
from .events import gerar_evento
from .boss_ai import boss_strategy
from .dungeon import gerar_dungeon
from .world_map import gerar_tile
from .inventory import gerar_item
from .npc_ai import npc_response
from .quests import gerar_quest
from .models import WorldState


# ==========================================================
# LOAD ÚNICO DO MODELO
# ==========================================================

_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model


# ==========================================================
# ÂNCORAS SEMÂNTICAS
# ==========================================================

ANCHORS = None


def build_anchors():

    model = get_model()

    return {
        "combate": model.encode("luta batalha ataque violência confronto"),
        "magia": model.encode("feitiço magia energia mística poder arcano"),
        "drama": model.encode("tensão medo silêncio suspense perigo"),
    }


def get_anchors():
    global ANCHORS

    if ANCHORS is None:
        ANCHORS = build_anchors()

    return ANCHORS


# ==========================================================
# WORLD STATE PERSISTENTE
# ==========================================================

def get_room(room_id):

    obj, created = WorldState.objects.get_or_create(
        room_id=room_id
    )

    return {
        "boss_hp": obj.boss_hp,
        "fase": obj.fase,
        "entropia": obj.entropia,
        "obj": obj
    }


def save_room(room):

    obj = room["obj"]

    obj.boss_hp = room["boss_hp"]
    obj.fase = room["fase"]
    obj.entropia = room["entropia"]

    obj.save()


# ==========================================================
# DETECÇÃO DE TOM SEMÂNTICO
# ==========================================================

def detectar_tom(texto):

    model = get_model()
    anchors = get_anchors()

    vetor = model.encode(texto)

    scores = {}

    for chave, anchor in anchors.items():

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
# UTILIDADES DE COMBATE
# ==========================================================

def rolar_d20():
    return random.randint(1, 20)


def calcular_dano(base=8):
    return random.randint(base - 3, base + 3)


# ==========================================================
# FASE DO BOSS
# ==========================================================

def atualizar_fase(room):

    hp = room["boss_hp"]

    if hp < 40:
        room["fase"] = 3

    elif hp < 80:
        room["fase"] = 2

    else:
        room["fase"] = 1


# ==========================================================
# NARRATIVA DO BOSS
# ==========================================================

def narrar_boss(room):

    strategy = boss_strategy(room)

    if strategy == "defensivo":
        return "A criatura mantém distância, analisando cada movimento."

    elif strategy == "agressivo":
        return "Ferido, o monstro avança com fúria crescente."

    else:
        return "A criatura perde o controle e ataca caoticamente."


# ==========================================================
# CRIAR SESSÃO
# ==========================================================

def criar_sessao(nome, classe, room_id):

    get_room(room_id)

    personagem = {
        "nome": nome,
        "classe": classe,
        "hp": 100,
        "mana": 60,
        "xp": 0,
        "inventario": []
    }

    return {
        "session_id": f"{room_id}_{nome}",
        "personagem": personagem
    }


# ==========================================================
# MOTOR NARRATIVO
# ==========================================================

def analisar_qwan_narrativo(textos, room_id="default"):

    texto = textos[0]

    room = get_room(room_id)

    tom = detectar_tom(texto)

    narrativa = narrar_acao(texto, tom)

    # ===============================
    # MEMÓRIA NARRATIVA
    # ===============================

    remember(room_id, texto)

    memoria = recall(room_id)

    # ===============================
    # ENTROPIA DO MUNDO
    # ===============================

    room["entropia"] += 0.05
    room["entropia"] = min(room["entropia"], 1)

    # ===============================
    # EVENTO PROCEDURAL
    # ===============================

    evento = gerar_evento(room["entropia"])

    if evento:
        narrativa += f"\n\n⚡ Evento: {evento}"

    # ===============================
    # DUNGEON PROCEDURAL
    # ===============================

    depth = int(room["entropia"] * 10)

    dungeon = gerar_dungeon(room_id, depth)

    narrativa += f"\n\n🗺️ Local: {dungeon['descricao']} ({dungeon['bioma']})"

    # ===============================
    # MAPA PROCEDURAL
    # ===============================

    x = random.randint(-50, 50)
    y = random.randint(-50, 50)

    tile = gerar_tile(x, y)

    narrativa += f"\n🌍 Região próxima: {tile['bioma']} (perigo {tile['perigo']})"

    # ===============================
    # ITEM PROCEDURAL
    # ===============================

    if random.random() < 0.2:

        item = gerar_item(room["entropia"])

        narrativa += f"\n\n🎒 Você encontrou: {item['nome']} ({item['raridade']})"

    # ===============================
    # QUEST PROCEDURAL
    # ===============================

    if random.random() < 0.1:

        quest = gerar_quest(texto)

        narrativa += f"\n\n📜 Nova missão: {quest['quest']}"

    # ===============================
    # ECO DA MEMÓRIA
    # ===============================

    if len(memoria) > 5:

        eco = random.choice(memoria[-5:])

        narrativa += f"\n\n💭 Algo nesta cena lembra: \"{eco[:60]}...\""

    save_room(room)

    return {
        "narrativa": narrativa.strip(),
        "entropia": room["entropia"],
        "memoria": memoria[-5:]
    }


# ==========================================================
# COMBATE
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

    # ===============================
    # ENTROPIA DE COMBATE
    # ===============================

    room["entropia"] += 0.02
    room["entropia"] = min(room["entropia"], 1)

    # ===============================
    # EVENTO DURANTE COMBATE
    # ===============================

    evento = gerar_evento(room["entropia"])

    if evento:
        narrativa += f"\n\n⚡ O ambiente reage: {evento}"

    # ===============================
    # LOOT
    # ===============================

    if sucesso and random.random() < 0.25:

        item = gerar_item(room["entropia"])

        narrativa += f"\n\n💎 Loot obtido: {item['nome']} ({item['raridade']})"

    save_room(room)

    return {
        "narrativa": narrativa.strip(),
        "hp": 100,
        "mana": 60,
        "xp": 10 if sucesso else 0,
        "hp_inimigo": max(room["boss_hp"], 0),
        "fase_boss": room["fase"],
        "entropia": room["entropia"]
    }


# ==========================================================
# INTERAÇÃO COM NPC
# ==========================================================

def conversar_npc(npc_id, texto):

    resposta = npc_response(npc_id, texto)

    return {
        "npc_id": npc_id,
        "resposta": resposta
    }
