import random
import uuid

PERSONALIDADES = [

"mercador ganancioso",
"sábio misterioso",
"aventureiro aposentado",
"sacerdote devoto",
"trapaceiro"

]


def gerar_npc(cidade_id):

    return {

        "id": str(uuid.uuid4()),

        "cidade": cidade_id,

        "personalidade": random.choice(PERSONALIDADES),

        "relacao": 0.5,

        "memoria": []

    }
