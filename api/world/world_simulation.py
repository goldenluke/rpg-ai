# api/world/world_simulation.py

import random
import threading
import time


WORLD = {

    "cities": {},
    "npcs": {},
    "factions": {},
    "quests": {},
    "history": []

}


CITY_NAMES = [

    "Aldoria",
    "Drakmoor",
    "Velaris",
    "Eldhollow",
    "Ironhaven",
    "Ravenfall"

]


NPC_TYPES = [

    "mercador",
    "guerreiro",
    "mago",
    "ladino",
    "camponês"

]


QUESTS = [

    "Derrote o monstro",
    "Escolte a caravana",
    "Recupere artefato",
    "Explore ruínas",
    "Proteja a cidade"

]


FACTIONS = [

    "Ordem da Chama",
    "Irmandade Sombria",
    "Guilda Mercante",
    "Culto do Abismo"

]


# -----------------------------
# EVENTOS DO MUNDO
# -----------------------------


def world_event(text):

    WORLD["history"].append({

        "text": text

    })

    if len(WORLD["history"]) > 100:

        WORLD["history"].pop(0)


# -----------------------------
# GERAR CIDADE
# -----------------------------


def spawn_city():

    nome = random.choice(CITY_NAMES)

    if nome in WORLD["cities"]:
        return

    cidade = {

        "nome": nome,
        "pop": random.randint(100, 5000)

    }

    WORLD["cities"][nome] = cidade

    world_event(f"🏙 Cidade fundada: {nome}")


# -----------------------------
# GERAR NPC
# -----------------------------


def spawn_npc():

    npc_id = str(len(WORLD["npcs"]) + 1)

    npc = {

        "tipo": random.choice(NPC_TYPES),
        "nivel": random.randint(1, 10)

    }

    WORLD["npcs"][npc_id] = npc

    world_event(f"👤 Novo NPC apareceu: {npc['tipo']}")


# -----------------------------
# GERAR FACÇÃO
# -----------------------------


def spawn_faction():

    nome = random.choice(FACTIONS)

    if nome in WORLD["factions"]:
        return

    faction = {

        "nome": nome,
        "poder": random.randint(10, 100)

    }

    WORLD["factions"][nome] = faction

    world_event(f"🏳️ Facção surgiu: {nome}")


# -----------------------------
# GERAR QUEST
# -----------------------------


def spawn_quest():

    quest_id = str(len(WORLD["quests"]) + 1)

    quest = {

        "titulo": random.choice(QUESTS),
        "recompensa": random.randint(50, 200)

    }

    WORLD["quests"][quest_id] = quest

    world_event(f"📜 Nova quest: {quest['titulo']}")


# -----------------------------
# TICK DO MUNDO
# -----------------------------


def world_tick():

    r = random.random()

    if r < 0.25:
        spawn_city()

    elif r < 0.50:
        spawn_npc()

    elif r < 0.75:
        spawn_quest()

    else:
        spawn_faction()


# -----------------------------
# LOOP DE SIMULAÇÃO
# -----------------------------


def world_loop():

    while True:

        world_tick()

        time.sleep(10)


# -----------------------------
# INICIAR SIMULAÇÃO
# -----------------------------


def start_world():

    t = threading.Thread(target=world_loop)

    t.daemon = True

    t.start()
