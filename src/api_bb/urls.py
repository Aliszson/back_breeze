from django.urls import include, path
from rest_framework import routers

from api_bb.views import (
    AlbumViewSet,
    ArtistaViewSet,
    AvaliacaoViewSet,
    GeneroViewSet,
    MusicaViewSet,
    UsuarioViewSet,
)

router = routers.DefaultRouter()

router.register(r"generos", GeneroViewSet)
router.register(r"usuarios", UsuarioViewSet)
router.register(r"musicas", MusicaViewSet)
router.register(r"albuns", AlbumViewSet)
router.register(r"artistas", ArtistaViewSet)
router.register(r"avaliacoes", AvaliacaoViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
