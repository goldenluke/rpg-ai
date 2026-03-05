import random

TIPOS = [
"vilarejo",
"cidade mercantil",
"fortaleza",
"porto"
]

LOCAIS = [
"taverna",
"mercado",
"templo",
"guilda",
"estábulo"
]


def gerar_cidade(x,y):

    random.seed(x*10000+y)

    tipo=random.choice(TIPOS)

    locais=random.sample(LOCAIS,3)

    populacao=random.randint(50,5000)

    return{

    "tipo":tipo,
    "locais":locais,
    "populacao":populacao

    }
