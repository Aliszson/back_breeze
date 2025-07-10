from rest_framework import serializers

from .models import Album, Artista, Avaliacao, Genero, Musica, Usuario


class GeneroSerializer(serializers.ModelSerializer):
    """Serializa o modelo de gênero musical."""

    class Meta:
        model = Genero
        fields = ("id", "nome")


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializa o modelo de usuário, incluindo gêneros favoritos."""

    generos_favoritos = GeneroSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = (
            "id",
            "username",
            "email",
            "bio",
            "foto",
            "critico",
            "generos_favoritos",
        )
        
        read_only_fields = ("id", "email", "critico", "generos_favoritos")


class MusicaSerializer(serializers.ModelSerializer):
    """Serializa o modelo de música."""

    class Meta:
        model = Musica
        fields = ("id", "titulo", "letra", "duracao", "capa")


class AlbumSerializer(serializers.ModelSerializer):
    """Serializa o modelo de álbum, com gêneros e faixas embutidas."""

    genero_album = GeneroSerializer(many=True, read_only=True)
    faixa = MusicaSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ("id", "nome", "capa", "genero_album", "faixa")


class ArtistaSerializer(serializers.ModelSerializer):
    """Serializa o modelo de artista com seus gêneros e álbuns."""

    genero_artista = GeneroSerializer(many=True, read_only=True)
    albuns = AlbumSerializer(many=True, read_only=True)

    class Meta:
        model = Artista
        fields = ("id", "nome", "foto", "genero_artista", "albuns")


class AvaliacaoSerializer(serializers.ModelSerializer):
    """Serializa o modelo de avaliação de músicas ou álbuns."""

    class Meta:
        model = Avaliacao
        fields = (
            "id",
            "comentario",
            "data_avaliacao",
            "nota",
            "avaliador",
            "musica",
            "album",
        )
