from django.urls import include, path
from rest_framework import routers
from .views import (
    DeezerSearchView,
    MusicaDetalheView,
    AlbumViewSet,
    ArtistaViewSet,
    AvaliacaoViewSet,
    GeneroViewSet,
    MusicaViewSet,
    UsuarioViewSet,
    PerfilUsuarioView,
    TopBrasilView,
    TopMundoView,
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
    # Rota para a página de detalhes da música
    path('musica-detalhes/<int:deezer_id>/', MusicaDetalheView.as_view(), name='musica-detalhe'),
    
    # rotas para os gráficos de músicas mais tocadas
    path('charts/brasil/', TopBrasilView.as_view(), name='chart-brasil'),
    path('charts/mundo/', TopMundoView.as_view(), name='chart-mundo'),
]
