from django.contrib.auth.models import AbstractUser
from django.db import models


class Genero(models.Model):
    """Representa um gênero musical (ex: Rock, Pop, Samba)."""

    nome = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.nome}"


class Musica(models.Model):
    """
    Representa uma música com título, letra, duração e caminho da capa.
    """

    titulo = models.CharField(max_length=50)
    letra = models.TextField(max_length=900)
    duracao = models.IntegerField()
    capa = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.titulo}"


class Album(models.Model):
    """
    Representa um álbum musical, que contém várias faixas (músicas) e gêneros.
    """

    nome = models.CharField(max_length=50)
    capa = models.CharField(max_length=200)
    genero_album = models.ManyToManyField(Genero, blank=False)
    faixa = models.ManyToManyField(Musica, blank=False)

    def __str__(self):
        return f"{self.nome}"


class Usuario(AbstractUser):
    """
    Representa um usuário do sistema, que pode ou não ser crítico musical.
    """

    bio = models.TextField(max_length=200)
    foto = models.CharField(max_length=200)
    critico = models.BooleanField(default=False)
    generos_favoritos = models.ManyToManyField(Genero, blank=True)

    def __str__(self):
        return f"{self.username}"


class Artista(models.Model):
    """
    Representa um artista musical, que possui gêneros e álbuns associados.
    """

    nome = models.CharField(max_length=20)
    foto = models.CharField(max_length=200)
    generos_artista = models.ManyToManyField(Genero, blank=False)
    albuns = models.ManyToManyField(Album, blank=True)

    def __str__(self):
        return f"{self.nome}"


class Avaliacao(models.Model):
    """
    Representa a avaliação feita por um usuário sobre uma música ou álbum.
    """

    comentario = models.TextField(max_length=200)
    data_avaliacao = models.DateTimeField(auto_now_add=True)
    nota = models.IntegerField()
    avaliador = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=False)
    musica = models.ForeignKey(Musica, on_delete=models.CASCADE, blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.avaliador} - {self.comentario} - {self.album}"
