from rest_framework import viewsets

from .models import *
from .serializers import (
    AlbumSerializer,
    ArtistaSerializer,
    AvaliacaoSerializer,
    GeneroSerializer,
    MusicaSerializer,
    UsuarioSerializer,
)


class GeneroViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar, criar, editar e deletar gêneros musicais.
    """

    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar, criar, editar e deletar usuários.
    """

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class MusicaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar, criar, editar e deletar músicas.
    """

    queryset = Musica.objects.all()
    serializer_class = MusicaSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar, criar, editar e deletar álbuns.
    """

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class ArtistaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar, criar, editar e deletar artistas.
    """

    queryset = Artista.objects.all()
    serializer_class = ArtistaSerializer


class AvaliacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar, criar, editar e deletar avaliações de músicas ou álbuns.
    """

    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
