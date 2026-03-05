from django.contrib import admin
from django.urls import path

from api.views import (

    dashboard_view,

    criar_sessao_view,
    analisar_cena,
    combate_view,

    map_view,
    monster_view,
    dungeon_view,
    faction_view,
    world_state_view

)
from api.views import history_view

urlpatterns = [

    # admin
    path("admin/", admin.site.urls),
    path("api/world/history", history_view),
    # dashboard
    path("", dashboard_view),
    path("dashboard/", dashboard_view),

    # RPG
    path("api/rpg/criar-sessao", criar_sessao_view),
    path("api/rpg/analisar-cena", analisar_cena),
    path("api/rpg/combate", combate_view),

    # WORLD ENGINE
    path("api/world/map", map_view),
    path("api/world/monster", monster_view),
    path("api/world/dungeon", dungeon_view),
    path("api/world/faction", faction_view),
    path("api/world/state", world_state_view),

]
