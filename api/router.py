# api/views.py
from ninja import Router, Schema
from .engine import buscar_contexto_rpg

router = Router()

# Schema para validar o que o Bot envia
class NarrativaSchema(Schema):
    texto: str

@router.post("/analisar-cena")
def analisar_cena(request, data: NarrativaSchema):
    resultado = buscar_contexto_rpg(data.texto)
    return {
        "status": "sucesso",
        "regra_detectada": resultado["regra"],
        "detalhes": resultado["descricao"]
    }

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/rpg/(?P<room_id>\w+)/$', consumers.RPGConsumer.as_asgi()),
]
