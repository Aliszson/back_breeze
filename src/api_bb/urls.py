from django.urls import include, path
from rest_framework import routers
from api_bb.views import UsuarioViewSet 

router = routers.DefaultRouter()

router.register(r"usuarios", UsuarioViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
