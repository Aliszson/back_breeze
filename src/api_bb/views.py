import requests
from rest_framework import viewsets
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response

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
    
class DeezerSearchView(APIView):
    """
    Uma view que atua como proxy para a API de busca do Deezer.
    """
    # Como é uma busca pública, podemos permitir que qualquer usuário (mesmo não autenticado)
    # a utilize. Djoser/DRF cuidará da autenticação para outros endpoints.
    permission_classes = [] 
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        # 1. Pega o termo de busca dos parâmetros da URL (?q=termo)
        search_term = request.query_params.get('q', None)

        if not search_term:
            return Response(
                {"error": "O parâmetro de busca 'q' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Monta e faz a requisição para a API do Deezer
        deezer_api_url = "https://api.deezer.com/search"
        params = {'q': search_term}

        try:
            response = requests.get(deezer_api_url, params=params)
            response.raise_for_status()  # Lança um erro para status HTTP 4xx/5xx

            # 3. Retorna os dados do Deezer diretamente para o frontend
            deezer_data = response.json()
            return Response(deezer_data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            # Em caso de erro de conexão ou da API do Deezer
            return Response(
                {"error": f"Erro ao contatar a API do Deezer: {e}"},
                status=status.HTTP_502_BAD_GATEWAY # "Bad Gateway", pois nosso servidor depende de outro
            )
