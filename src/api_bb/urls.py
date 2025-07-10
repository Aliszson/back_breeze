from django.urls import include, path
from rest_framework import routers
from .views import DeezerSearchView

from api_bb.views import (
    AlbumViewSet,
    ArtistaViewSet,
    AvaliacaoViewSet,
    GeneroViewSet,
    MusicaViewSet,
    UsuarioViewSet,
    PerfilUsuarioView,
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
    path('search/', DeezerSearchView.as_view(), name='deezer-search'),
    path('auth/users/me/', PerfilUsuarioView.as_view(), name='perfil-usuario'),
]
