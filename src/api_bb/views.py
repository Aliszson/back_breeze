import requests
from rest_framework import viewsets, generics, status, permissions, parsers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Musica, Avaliacao, Genero, Usuario, Album, Artista

from .serializers import (
    MusicaDetalheSerializer,
    AvaliacaoSerializer,
    GeneroSerializer,
    UsuarioSerializer,
    MusicaSerializer,
    AlbumSerializer,
    ArtistaSerializer,
)

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PerfilUsuarioView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    def get_object(self):
        return self.request.user

class MusicaViewSet(viewsets.ModelViewSet):
    """ViewSet para o modelo Musica (usado principalmente pelo router)."""
    queryset = Musica.objects.all()
    serializer_class = MusicaSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class ArtistaViewSet(viewsets.ModelViewSet):
    queryset = Artista.objects.all()
    serializer_class = ArtistaSerializer

class AvaliacaoViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar avaliações (Listar, Criar, etc.)."""
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        ✅ MODIFICADO: Esta função sobrescreve o comportamento padrão.
        Ela filtra o queryset para retornar apenas as avaliações
        feitas pelo usuário que está logado.
        """
        user = self.request.user
        return Avaliacao.objects.filter(avaliador=user)
    
    def perform_create(self, serializer):
        """Associa o usuário logado automaticamente ao criar uma avaliação."""
        serializer.save(avaliador=self.request.user)

class DeezerSearchView(APIView):
    permission_classes = []
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        search_term = request.query_params.get('q', None)
        if not search_term:
            return Response({"error": "O parâmetro de busca 'q' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        deezer_api_url = "https://api.deezer.com/search"
        params = {'q': search_term}
        try:
            response = requests.get(deezer_api_url, params=params)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Erro ao contatar a API do Deezer: {e}"}, status=status.HTTP_502_BAD_GATEWAY)

class MusicaDetalheView(APIView):
    """View para buscar ou criar uma música e retornar seus detalhes."""
    permission_classes = [IsAuthenticated]
    def get(self, request, deezer_id):
        try:
            musica = Musica.objects.get(deezer_id=deezer_id)
        except Musica.DoesNotExist:
            deezer_response = requests.get(f"https://api.deezer.com/track/{deezer_id}")
            if deezer_response.status_code != 200:
                return Response({"error": "Música não encontrada no Deezer"}, status=status.HTTP_404_NOT_FOUND)
            data = deezer_response.json()
            if 'error' in data:
                return Response({"error": "Música não encontrada no Deezer"}, status=status.HTTP_404_NOT_FOUND)
            musica = Musica.objects.create(
                deezer_id=data['id'],
                titulo=data['title'],
                duracao=data['duration'],
                capa_url=data.get('album', {}).get('cover_big', ''),
                link_deezer=data.get('link', ''),
                artista_nome=data.get('artist', {}).get('name', 'Desconhecido'),
                album_nome=data.get('album', {}).get('title', 'Desconhecido')
            )
        serializer = MusicaDetalheSerializer(musica, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TopBrasilView(APIView):
    """
    View que atua como proxy para buscar o chart 'Top Brasil' do Deezer.
    """
    permission_classes = [] # É um chart público
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        deezer_url = "https://api.deezer.com/playlist/13278689463/tracks"
        try:
            response = requests.get(deezer_url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Erro ao contatar a API do Deezer: {e}"}, status=status.HTTP_502_BAD_GATEWAY)


class TopMundoView(APIView):
    """
    View que atua como proxy para buscar o chart 'Top Mundo' do Deezer.
    """
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        deezer_url = "https://api.deezer.com/playlist/3155776842/tracks"
        try:
            response = requests.get(deezer_url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Erro ao contatar a API do Deezer: {e}"}, status=status.HTTP_502_BAD_GATEWAY)
