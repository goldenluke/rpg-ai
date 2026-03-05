import random


EVENTOS_BIOMA = {

"floresta":[
"Você encontra pegadas estranhas entre as árvores.",
"Um cervo observa você antes de desaparecer na vegetação.",
"Uma cabana abandonada surge entre as árvores."
],

"montanhas":[
"Uma avalanche distante ecoa pelo vale.",
"Um ninho de águia gigante domina o penhasco.",
"Uma trilha antiga leva a ruínas esquecidas."
],

"deserto":[
"Uma tempestade de areia surge no horizonte.",
"Um viajante perdido pede água.",
"Você encontra ossos antigos enterrados na areia."
],

"pântano":[
"Algo se move sob a água escura.",
"Um sapo gigante observa você.",
"Uma luz fantasmagórica surge entre a névoa."
]

}


def gerar_evento(tile):

    bioma = tile["bioma"]

    if bioma not in EVENTOS_BIOMA:
        return None

    evento = random.choice(EVENTOS_BIOMA[bioma])

    return {
        "tipo":"exploracao",
        "descricao":evento
    }
