from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

from .engine import (
    analisar_qwan_narrativo,
    criar_sessao,
    combate,
    SESSOES
)

# ==========================================================
# INDEX
# ==========================================================

def index_view(request):
    return render(request, "index.html")


# ==========================================================
# DASHBOARD
# ==========================================================

def dashboard_view(request):
    return JsonResponse({
        "status": "RPG Engine Online",
        "sessoes_ativas": len(SESSOES)
    })


# ==========================================================
# CRIAR SESSÃO
# ==========================================================

@csrf_exempt
def criar_sessao_view(request):

    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    body = json.loads(request.body)

    nome = body.get("nome", "Aventureiro")
    classe = body.get("classe", "guerreiro")

    resultado = criar_sessao(nome, classe)

    return JsonResponse(resultado)


# ==========================================================
# ANALISAR CENA
# ==========================================================

@csrf_exempt
def analisar_cena(request):

    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    body = json.loads(request.body)
    textos = body.get("textos", [])

    resultado = analisar_qwan_narrativo(textos)

    return JsonResponse({
        "narrativa": resultado["cena"]["texto"],
        "regime": resultado["cena"]["regime"],
        "nivel_campanha": resultado["cena"]["nivel_campanha"],
        "escolhas": resultado["cena"]["escolhas"]
    })


# ==========================================================
# COMBATE
# ==========================================================

@csrf_exempt
def combate_view(request):

    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    body = json.loads(request.body)

    session_id = body.get("session_id")
    acao = body.get("acao", "Atacar")

    resultado = combate(session_id, acao)

    return JsonResponse(resultado)
