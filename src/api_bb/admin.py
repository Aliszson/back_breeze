from django.contrib import admin

# Register your models here.

from .models import Genero, Musica, Album, Usuario, Artista, Avaliacao

# registro de cada modelo para que ele apareça na interface de admin
admin.site.register(Genero)
admin.site.register(Musica)
admin.site.register(Album)
admin.site.register(Usuario) 
admin.site.register(Artista)
admin.site.register(Avaliacao)
