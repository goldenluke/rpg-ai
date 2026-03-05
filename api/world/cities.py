import random
import uuid

CITY_NAMES = [
"Arkhon",
"Valdora",
"Thalmar",
"Eldwyn",
"Karthis"
]


def gerar_cidade(x,y):

    city_id = str(uuid.uuid4())

    return {

        "id": city_id,

        "nome": random.choice(CITY_NAMES),

        "x": x,
        "y": y,

        "populacao": random.randint(50,300),

        "riqueza": random.random(),

        "lojas": []
    }
