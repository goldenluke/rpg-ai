from django.contrib import admin
from django.urls import path

from api.views import (
    index_view,
    dashboard_view,
    analisar_cena,
    criar_sessao_view,
    combate_view,
)

urlpatterns = [
    path("", index_view),
    path("admin/", admin.site.urls),
    path("dashboard/", dashboard_view),

    path("api/rpg/criar-sessao", criar_sessao_view),
    path("api/rpg/analisar-cena", analisar_cena),
    path("api/rpg/combate", combate_view),
]
