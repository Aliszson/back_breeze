from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Genero(models.Model):
    #id_genero = models.IntegerField()
    nome = models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.nome}"
    
class Musica(models.Model):
    #id_musica = models.IntegerField()
    titulo = models.CharField(max_length=50)
    letra = models.TextField()
    duracao = models.IntegerField()
    capa = models.CharField()
    
    def __str__(self):
        return f"{self.titulo}"
   
class Album(models.Model):
    #id_album = models.IntegerField()
    nome = models.CharField(max_length=50)
    capa = models.CharField()
    
    genero_album = models.ManyToManyField(
        Genero, blank=False,null=False
    )
    
    faixa = models.ManyToManyField(
        Musica, blank=False,null=False
    )
    
    def __str__(self):
        return f"{self.nome}" 
    
class Usuario(models.Model):
    #id_usuario = models.IntegerField()
    nome = models.CharField(max_length=10)
    bio = models.TextField(max_length=200)
    foto = models.CharField()
    critico = models.BooleanField(default=False)
    
    genero_favoritos = models.ManyToManyField(
        Genero, blank=True
    )
    
    def __str__(self):
        return f"{self.nome}"

class Artista(models.Model):
    #id_artista = models.IntegerField()
    nome = models.CharField(max_length=20)
    foto = models.CharField()
    
    generos_artista = models.ManyToManyField(
        Genero, blank=False
    )
    
    albuns = models.ManyToManyField(
        Album, blank=True
    )
    
    def __str__(self):
        return f"{self.nome}"
    
class Avaliacao(models.Model):
    #id_avaliacao = models.IntegerField
    comentario = models.TextField(max_length=200)
    data_avaliacao = models.DateTimeField(auto_now_add=True)
    nota = models.IntegerField()
    
    avaliador = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, blank=False,null=False
    )
    
    musica = models.ForeignKey(
        Musica, on_delete=models.CASCADE, blank=True,null=True
    )
    
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, blank=True,null=True
    )
    
    def __str__(self):
        return f"{self.avaliador} - {self.comentario} - {self.album}"