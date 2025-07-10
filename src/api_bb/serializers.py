from rest_framework import serializers
from django.db.models import Avg
from .models import Album, Artista, Avaliacao, Genero, Musica, Usuario


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ("id", "nome")


class UsuarioSerializer(serializers.ModelSerializer):
    generos_favoritos = GeneroSerializer(many=True, read_only=True)
    class Meta:
        model = Usuario
        fields = ("id", "username", "email", "bio", "foto", "critico", "generos_favoritos")
        read_only_fields = ("id", "email", "critico", "generos_favoritos")


class MusicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musica
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    genero_album = GeneroSerializer(many=True, read_only=True)
    faixa = MusicaSerializer(many=True, read_only=True)
    class Meta:
        model = Album
        fields = ("id", "nome", "capa", "genero_album", "faixa")


class ArtistaSerializer(serializers.ModelSerializer):
    genero_artista = GeneroSerializer(many=True, read_only=True)
    albuns = AlbumSerializer(many=True, read_only=True)
    class Meta:
        model = Artista
        fields = ("id", "nome", "foto", "genero_artista", "albuns")


class UsuarioSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'foto']


class AvaliacaoSerializer(serializers.ModelSerializer):
    # --- CAMPO PARA LEITURA (Mostrar detalhes) ---
    musica = MusicaSerializer(read_only=True)
    avaliador = UsuarioSimplesSerializer(read_only=True)

    # --- CAMPO PARA ESCRITA (Receber ID ao criar) ---
    musica_id = serializers.PrimaryKeyRelatedField(
        queryset=Musica.objects.all(), source='musica', write_only=True
    )

    class Meta:
        model = Avaliacao
        # Adicionado 'musica_id' para a escrita
        fields = ("id", "comentario", "data_avaliacao", "nota", "avaliador", "musica", "musica_id")
        read_only_fields = ("avaliador", "data_avaliacao")

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            musica_instance = data.get('musica')
            if Avaliacao.objects.filter(musica=musica_instance, avaliador=user).exists():
                raise serializers.ValidationError("Você já avaliou esta música.")
        return data


class MusicaDetalheSerializer(serializers.ModelSerializer):
    avaliacoes = AvaliacaoSerializer(many=True, read_only=True)
    media_avaliacoes = serializers.SerializerMethodField()
    avaliado_pelo_usuario = serializers.SerializerMethodField()

    class Meta:
        model = Musica
        fields = [
            'id', 'deezer_id', 'titulo', 'duracao', 'capa_url',
            'link_deezer', 'artista_nome', 'album_nome', 'avaliacoes',
            'media_avaliacoes', 'avaliado_pelo_usuario'
        ]

    def get_media_avaliacoes(self, obj):
        media = obj.avaliacoes.aggregate(Avg('nota')).get('nota__avg')
        return round(media, 1) if media is not None else None

    def get_avaliado_pelo_usuario(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Avaliacao.objects.filter(musica=obj, avaliador=request.user).exists()
        return False
