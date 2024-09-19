from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Producto, Mascota, Cliente
from .serializers import ProductoSerializer, MascotaSerializer, ClienteSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User

# Registro de usuarios (sin autenticación)
@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir acceso a cualquier usuario
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Verificar si el usuario ya existe
    if User.objects.filter(username=username).exists():
        return Response({'detail': 'El usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)

    # Crear nuevo usuario
    user = User.objects.create_user(username=username, password=password)
    
    # Generar tokens de acceso y refresco
    refresh = RefreshToken.for_user(user)

    # Devolver los tokens de acceso y refresco
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }, status=status.HTTP_201_CREATED)


# Producto ViewSet para gestionar el modelo Producto
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Cliente ViewSet para gestionar el modelo Cliente
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

# Mascota ViewSet para gestionar el modelo Mascota
class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
