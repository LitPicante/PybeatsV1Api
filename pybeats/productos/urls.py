from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import mascotas_list_create, eliminar_mascota
from .views import clientes_list_create, eliminar_cliente, register_user  # Importa register_user
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)  # Registra el ViewSet

urlpatterns = [
    path('', include(router.urls)),  # Incluye el enrutador
    # Aquí mantienes las otras rutas para mascotas y clientes
    path('mascotas/', mascotas_list_create, name='mascotas_list_create'),
    path('mascotas/<int:pk>/', eliminar_mascota, name='eliminar_mascota'),
    path('clientes/', clientes_list_create, name='clientes_list_create'),
    path('clientes/<int:pk>/', eliminar_cliente, name='eliminar_cliente'),
    
    # Ruta para el registro de usuarios (sin duplicar el prefijo 'api/')
    path('register/', register_user, name='register_user'),
    
    # Rutas para autenticación JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]




