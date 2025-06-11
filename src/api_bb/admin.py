from django.contrib import admin

from .models import Album, Artista, Avaliacao, Genero, Musica, Usuario

# Register your models here.


# registro de cada modelo para que ele apareça na interface de admin
admin.site.register(Genero)
admin.site.register(Musica)
admin.site.register(Album)
admin.site.register(Usuario)
admin.site.register(Artista)
admin.site.register(Avaliacao)
