from django.contrib.auth.models import AbstractUser
from django.db import models


class Genero(models.Model):
    """Representa um gênero musical (ex: Rock, Pop, Samba)."""
    nome = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.nome}"


class Musica(models.Model):
    """
    Representa uma música com dados vindos da API do Deezer.
    """
    deezer_id = models.BigIntegerField(unique=True, db_index=True)
    titulo = models.CharField(max_length=200)
    duracao = models.IntegerField()
    capa_url = models.URLField(max_length=500, blank=True)
    link_deezer = models.URLField(max_length=500, blank=True)
    artista_nome = models.CharField(max_length=200)
    
    album_nome = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.titulo} - {self.artista_nome}"


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
    bio = models.TextField(max_length=160, blank=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
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
    Representa a avaliação feita por um usuário sobre uma música.
    """
    comentario = models.TextField(max_length=200, blank = True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)
    nota = models.IntegerField()
    avaliador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    musica = models.ForeignKey(Musica, on_delete=models.CASCADE, related_name="avaliacoes")

    class Meta:
        ordering = ['-data_avaliacao']
        unique_together = ('avaliador', 'musica')

    def __str__(self):
        return f"{self.avaliador.username} - {self.musica.titulo}"
