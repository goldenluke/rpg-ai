import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .engine import (
    criar_sessao,
    analisar_qwan_narrativo,
    combate
)


# ==========================================================
# CRIAR SESSÃO
# ==========================================================

@csrf_exempt
def criar_sessao_view(request):
    if request.method == "POST":
        data = json.loads(request.body)

        nome = data.get("nome")
        classe = data.get("classe")
        room_id = data.get("room_id", "default")

        resultado = criar_sessao(nome, classe, room_id)

        return JsonResponse(resultado)

    return JsonResponse({"erro": "Método inválido"})


# ==========================================================
# ANALISAR CENA (NARRATIVO)
# ==========================================================



@csrf_exempt
def analisar_cena(request):
    if request.method == "POST":
        data = json.loads(request.body)

        textos = data.get("textos", [])
        room_id = data.get("room_id", "default")

        resultado = analisar_qwan_narrativo(textos, room_id)

        return JsonResponse({
            "narrativa": resultado["narrativa"]
        })

    return JsonResponse({"erro": "Método inválido"})


# ==========================================================
# COMBATE
# ==========================================================

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


from django.shortcuts import render

def dashboard_view(request):
    return render(request, "index.html")
