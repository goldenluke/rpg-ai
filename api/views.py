import json
import random

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .engine import (
    criar_sessao,
    analisar_qwan_narrativo,
    combate
)

from api.world.map import get_tile
from api.world.history_store import add_history, get_history

from api.world.world_simulation import WORLD


def world_state_view(request):

    return JsonResponse({

        "world": WORLD

    })

# ===============================
# DASHBOARD
# ===============================

def dashboard_view(request):

    return render(request, "index.html")


# ===============================
# CRIAR SESSÃO
# ===============================

@csrf_exempt
def criar_sessao_view(request):

    if request.method == "POST":

        data = json.loads(request.body)

        nome = data.get("nome", "Aventureiro")
        classe = data.get("classe", "guerreiro")
        room_id = data.get("room_id", "default")

        resultado = criar_sessao(nome, classe, room_id)

        return JsonResponse(resultado)

    return JsonResponse({"erro": "Método inválido"})


# ===============================
# ANALISAR CENA
# ===============================

@csrf_exempt
def analisar_cena(request):

    if request.method == "POST":

        data = json.loads(request.body)

        textos = data.get("textos", [])
        room_id = data.get("room_id", "default")

        resultado = analisar_qwan_narrativo(textos, room_id)

        evento = {
            "prompt": textos[0],
            "resposta": resultado["narrativa"]
        }

        add_history(evento)

        return JsonResponse({
            "narrativa": resultado["narrativa"]
        })


# ===============================
# COMBATE
# ===============================

def history_view(request):

    return JsonResponse({

        "history": get_history()

    })

@csrf_exempt
def combate_view(request):

    if request.method == "POST":

        data = json.loads(request.body)

        session_id = data.get("session_id")
        acao = data.get("acao")
        room_id = data.get("room_id", "default")

        resultado = combate(session_id, acao, room_id)

        return JsonResponse(resultado)

    return JsonResponse({"erro": "Método inválido"})


# ===============================
# MAPA PROCEDURAL
# ===============================

def map_view(request):

    x = int(request.GET.get("x", 0))
    y = int(request.GET.get("y", 0))

    tile = get_tile(x, y)

    return JsonResponse(tile)


# ===============================
# MONSTROS
# ===============================

def monster_view(request):

    monsters = [

        "Goblin",
        "Orc",
        "Slime",
        "Esqueleto",
        "Lobo Sombrio",
        "Aranha Gigante"

    ]

    monster = {

        "tipo": random.choice(monsters),
        "hp": random.randint(30, 120)

    }

    return JsonResponse({

        "monster": monster

    })


# ===============================
# DUNGEON
# ===============================

def dungeon_view(request):

    salas = random.randint(5, 15)

    dungeon = {

        "salas": list(range(salas)),
        "nivel": random.randint(1, 5)

    }

    return JsonResponse({

        "dungeon": dungeon

    })


# ===============================
# FACÇÕES
# ===============================

def faction_view(request):

    faccoes = [

        "Ordem da Chama",
        "Irmandade Sombria",
        "Guilda Mercante",
        "Culto do Abismo",
        "Guardiões da Floresta"

    ]

    faction = {

        "nome": random.choice(faccoes),
        "poder": random.randint(1, 100)

    }

    return JsonResponse({

        "faction": faction

    })


# ===============================
# ESTADO DO MUNDO
# ===============================

WORLD = {

    "cities": {},
    "npcs": {},
    "factions": {},
    "quests": {},
    "history": []

}


def world_state_view(request):

    return JsonResponse({

        "world": WORLD

    })
