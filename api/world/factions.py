# api/world/factions.py

import random
import uuid
from typing import Dict, Any, Optional

from .world_state import WORLD, log_event


FACTION_NAMES = [
    "Império de Arkhon",
    "Guilda dos Mercadores",
    "Culto Sombrio",
    "Ordem da Aurora",
    "Clã das Montanhas",
]


DEFAULT_RELATIONS = ["aliado", "neutro", "hostil"]


def generate_faction() -> Dict[str, Any]:
    """
    Gera uma facção procedural.
    """
    faction_id = str(uuid.uuid4())

    faction = {
        "id": faction_id,
        "nome": random.choice(FACTION_NAMES),
        "poder": round(random.uniform(0.3, 0.9), 2),
        "riqueza": round(random.uniform(0.2, 1.0), 2),
        "territorio": [],
        "reputacao_jogador": 0.0,
        "relacoes": {}  # faction_id -> relação
    }

    return faction


def register_faction(faction: Dict[str, Any]) -> str:
    """
    Registra a facção no estado do mundo.
    """
    fid = faction["id"]

    WORLD["factions"][fid] = faction

    log_event(f"A facção '{faction['nome']}' surgiu no mundo.", "faction")

    return fid


def change_player_reputation(faction_id: str, delta: float):
    """
    Ajusta reputação do jogador com uma facção.
    """
    faction = WORLD["factions"].get(faction_id)

    if not faction:
        return

    faction["reputacao_jogador"] += delta

    log_event(
        f"Reputação com {faction['nome']} mudou para {faction['reputacao_jogador']:.2f}",
        "faction"
    )


def set_relation(f1: str, f2: str, relation: Optional[str] = None):
    """
    Define relação entre duas facções.
    """
    if relation is None:
        relation = random.choice(DEFAULT_RELATIONS)

    if f1 not in WORLD["factions"] or f2 not in WORLD["factions"]:
        return

    WORLD["factions"][f1]["relacoes"][f2] = relation
    WORLD["factions"][f2]["relacoes"][f1] = relation

    log_event(
        f"As facções {WORLD['factions'][f1]['nome']} e "
        f"{WORLD['factions'][f2]['nome']} agora são {relation}.",
        "faction"
    )


def faction_tick():
    """
    Pequena simulação de poder e riqueza das facções.
    """
    for faction in WORLD["factions"].values():

        faction["riqueza"] += random.uniform(-0.02, 0.05)
        faction["poder"] += random.uniform(-0.02, 0.03)

        faction["riqueza"] = max(0.0, min(1.0, faction["riqueza"]))
        faction["poder"] = max(0.0, min(1.0, faction["poder"]))
