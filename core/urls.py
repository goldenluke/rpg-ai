from django.contrib import admin
from django.urls import path
from api.views import (
    criar_sessao_view,
    analisar_cena,
    combate_view,
    dashboard_view,
)

urlpatterns = [
    # Painel Admin
    path("admin/", admin.site.urls),

    # Dashboard (abre no root)
    path("", dashboard_view, name="home"),
    path("dashboard/", dashboard_view, name="dashboard"),

    # API RPG
    path("api/rpg/criar-sessao", criar_sessao_view, name="criar_sessao"),
    path("api/rpg/analisar-cena", analisar_cena, name="analisar_cena"),
    path("api/rpg/combate", combate_view, name="combate"),
]
