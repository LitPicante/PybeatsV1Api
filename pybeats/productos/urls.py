from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register_user  # Importa register_user
from rest_framework.routers import DefaultRouter

from .views import ProductoViewSet, ClienteViewSet, MascotaViewSet  # Importar los nuevos ViewSets

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)  # Registra el ViewSet de Producto
router.register(r'clientes', ClienteViewSet)    # Registra el ViewSet de Cliente
router.register(r'mascotas', MascotaViewSet)    # Registra el ViewSet de Mascota

urlpatterns = [
    path('', include(router.urls)),  # Incluye el enrutador
    # Ruta para el registro de usuarios
    path('register/', register_user, name='register_user'),
    
    # Rutas para autenticación JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]





