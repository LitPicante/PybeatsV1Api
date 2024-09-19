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


# Vista protegida para listar y crear clientes
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])  # Autenticación con JWT
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder
def clientes_list_create(request):
    if request.method == 'GET':
        # Listar todos los clientes
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Crear un nuevo cliente
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista protegida para eliminar un cliente por ID
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])  # Autenticación con JWT
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder
def eliminar_cliente(request, pk):
    try:
        # Buscar cliente por ID
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response({'detail': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Eliminar cliente
    cliente.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Vista protegida para listar y crear mascotas
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])  # Autenticación con JWT
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder
def mascotas_list_create(request):
    if request.method == 'GET':
        # Listar todas las mascotas
        mascotas = Mascota.objects.all()
        serializer = MascotaSerializer(mascotas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Crear una nueva mascota
        serializer = MascotaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista protegida para eliminar una mascota por ID
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])  # Autenticación con JWT
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder
def eliminar_mascota(request, pk):
    try:
        # Buscar mascota por ID
        mascota = Mascota.objects.get(pk=pk)
    except Mascota.DoesNotExist:
        return Response({'detail': 'Mascota no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    # Eliminar mascota
    mascota.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
