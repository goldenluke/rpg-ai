import random
from django.http import JsonResponse


def monster_view(request):

    monsters = [
        "Goblin",
        "Esqueleto",
        "Orc",
        "Slime",
        "Lobo Sombrio"
    ]

    monster = {
        "tipo": random.choice(monsters),
        "hp": random.randint(30, 80)
    }

    return JsonResponse({
        "monster": monster
    })
