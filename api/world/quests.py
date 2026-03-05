import random
import uuid

QUEST_TEMPLATES = [

"Derrote {enemy} perto de {cidade}",

"Entregue {item} para {npc}",

"Explore as ruínas de {cidade}"

]


def gerar_quest(cidade):

    template = random.choice(QUEST_TEMPLATES)

    return {

        "id": str(uuid.uuid4()),

        "descricao": template.format(
            enemy="goblin",
            cidade=cidade["nome"],
            npc="um mercador",
            item="uma relíquia"
        ),

        "recompensa": random.randint(20,100)

    }
