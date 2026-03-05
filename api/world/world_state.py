# api/world/world_state.py

import json
import time
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional

# Caminho padrão para persistência simples em JSON
BASE_DIR = Path(__file__).resolve().parents[2]
WORLD_FILE = BASE_DIR / "world_state.json"


# ==========================================================
# ESTRUTURA GLOBAL DO MUNDO
# ==========================================================

WORLD: Dict[str, Any] = {
    "meta": {
        "seed": None,
        "created_at": None,
        "last_tick": None,
        "version": 1
    },

    # Entidades principais
    "cities": {},     # city_id -> { ... }
    "npcs": {},       # npc_id -> { ... }
    "quests": {},     # quest_id -> { ... }
    "factions": {},   # faction_id -> { ... }

    # Sistemas globais
    "economy": {
        "prices": {},         # item -> preço médio global
        "demand": {},         # item -> nível de demanda
        "supply": {},         # item -> nível de oferta
        "last_update": None
    },

    # Histórico narrativo do mundo
    "history": [],   # lista de eventos narrativos

    # Métricas e telemetria simples
    "stats": {
        "cities_generated": 0,
        "npcs_generated": 0,
        "quests_generated": 0,
        "events_logged": 0,
        "ticks": 0
    }
}


# ==========================================================
# LOG DE EVENTOS DO MUNDO
# ==========================================================

def log_event(text: str, kind: str = "world", meta: Optional[Dict[str, Any]] = None):
    """
    Registra um evento narrativo ou sistêmico na história do mundo.
    """
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": time.time(),
        "kind": kind,
        "text": text,
        "meta": meta or {}
    }

    WORLD["history"].append(entry)
    WORLD["stats"]["events_logged"] += 1


def get_recent_history(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Retorna os últimos eventos do mundo.
    """
    return WORLD["history"][-limit:]


# ==========================================================
# CIDADES
# ==========================================================

def register_city(city: Dict[str, Any]) -> str:
    """
    Registra uma cidade no estado do mundo.
    """
    city_id = city.get("id") or str(uuid.uuid4())
    city["id"] = city_id

    WORLD["cities"][city_id] = city
    WORLD["stats"]["cities_generated"] += 1

    log_event(f"A cidade de {city.get('nome','Desconhecida')} foi fundada.", "city")

    return city_id


def get_city(city_id: str) -> Optional[Dict[str, Any]]:
    return WORLD["cities"].get(city_id)


def list_cities() -> List[Dict[str, Any]]:
    return list(WORLD["cities"].values())


# ==========================================================
# NPCS
# ==========================================================

def register_npc(npc: Dict[str, Any]) -> str:
    npc_id = npc.get("id") or str(uuid.uuid4())
    npc["id"] = npc_id

    WORLD["npcs"][npc_id] = npc
    WORLD["stats"]["npcs_generated"] += 1

    log_event(f"Um novo NPC surgiu: {npc.get('nome','desconhecido')}", "npc")

    return npc_id


def get_npc(npc_id: str) -> Optional[Dict[str, Any]]:
    return WORLD["npcs"].get(npc_id)


def list_npcs() -> List[Dict[str, Any]]:
    return list(WORLD["npcs"].values())


# ==========================================================
# QUESTS
# ==========================================================

def register_quest(quest: Dict[str, Any]) -> str:
    quest_id = quest.get("id") or str(uuid.uuid4())
    quest["id"] = quest_id

    WORLD["quests"][quest_id] = quest
    WORLD["stats"]["quests_generated"] += 1

    log_event(f"Nova missão disponível: {quest.get('descricao','missão desconhecida')}", "quest")

    return quest_id


def get_quest(quest_id: str) -> Optional[Dict[str, Any]]:
    return WORLD["quests"].get(quest_id)


def list_quests() -> List[Dict[str, Any]]:
    return list(WORLD["quests"].values())


# ==========================================================
# FACÇÕES
# ==========================================================

def register_faction(faction: Dict[str, Any]) -> str:
    faction_id = faction.get("id") or str(uuid.uuid4())
    faction["id"] = faction_id

    WORLD["factions"][faction_id] = faction

    log_event(f"A facção '{faction.get('nome','Desconhecida')}' foi registrada.", "faction")

    return faction_id


def get_faction(faction_id: str) -> Optional[Dict[str, Any]]:
    return WORLD["factions"].get(faction_id)


# ==========================================================
# ECONOMIA
# ==========================================================

def update_global_price(item: str, price: float):
    WORLD["economy"]["prices"][item] = price
    WORLD["economy"]["last_update"] = time.time()


def get_price(item: str) -> Optional[float]:
    return WORLD["economy"]["prices"].get(item)


# ==========================================================
# SIMULAÇÃO DO MUNDO
# ==========================================================

def world_tick():
    """
    Executa um passo da simulação do mundo.
    """
    now = time.time()

    WORLD["meta"]["last_tick"] = now
    WORLD["stats"]["ticks"] += 1

    # crescimento simples de cidades
    for city in WORLD["cities"].values():

        pop = city.get("populacao", 0)
        growth = max(1, int(pop * 0.01))

        city["populacao"] = pop + growth

    # pequenas flutuações econômicas
    for item, price in list(WORLD["economy"]["prices"].items()):

        delta = price * 0.05
        WORLD["economy"]["prices"][item] = max(1, price + (delta * (0.5 - time.time() % 1)))

    log_event("O mundo evoluiu um passo de simulação.", "simulation")


# ==========================================================
# PERSISTÊNCIA
# ==========================================================

def save_world(path: Path = WORLD_FILE):
    """
    Salva o estado do mundo em JSON.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(WORLD, f, indent=2)


def load_world(path: Path = WORLD_FILE):
    """
    Carrega estado do mundo salvo.
    """
    global WORLD

    if not path.exists():
        return

    with open(path, "r", encoding="utf-8") as f:
        WORLD = json.load(f)


# ==========================================================
# RESET (para debug)
# ==========================================================

def reset_world():
    """
    Reseta completamente o estado do mundo.
    """
    global WORLD

    WORLD = {
        "meta": {
            "seed": None,
            "created_at": time.time(),
            "last_tick": None,
            "version": 1
        },
        "cities": {},
        "npcs": {},
        "quests": {},
        "factions": {},
        "economy": {
            "prices": {},
            "demand": {},
            "supply": {},
            "last_update": None
        },
        "history": [],
        "stats": {
            "cities_generated": 0,
            "npcs_generated": 0,
            "quests_generated": 0,
            "events_logged": 0,
            "ticks": 0
        }
    }

    log_event("O mundo foi reiniciado.", "system")
