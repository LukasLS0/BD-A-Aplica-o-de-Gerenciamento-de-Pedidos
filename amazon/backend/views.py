from rest_framework import viewsets
from .models import Cliente, Vendedor, Produto, PerfilVendedor, Pedido, ItemPedido
from .serializers import ClienteSerializer, UsuarioSerializer, VendedorSerializer, ProdutoSerializer, PerfilVendedorSerializer, PedidoSerializer, ItemPedidoSerializer

from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
permission_classes)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Usuario
from .serializers import UsuarioSerializer
from .permissions import IsVendedor


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsVendedor()]

class PerfilVendedorViewSet(viewsets.ModelViewSet):
    queryset = PerfilVendedor.objects.select_related('vendedor').all()
    serializer_class = PerfilVendedorSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    def get_queryset(self):
        return (Pedido.objects
                .select_related('cliente')
                .prefetch_related('itens__produto')
                .all())

class ItemPedidoViewSet(viewsets.ModelViewSet):
    queryset = ItemPedido.objects.select_related('pedido', 'produto').all()
    serializer_class = ItemPedidoSerializer
    

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        usuario = serializer.save()
        token = Token.objects.create(user=usuario)
        return Response({'token': token.key, 'usuario': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    usuario = get_object_or_404(Usuario, username=request.data.get('username'))
    if not usuario.check_password(request.data.get('password')):
        return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=usuario)
    return Response({'token': token.key, 'usuario': UsuarioSerializer(usuario).data})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def perfil(request):
    return Response({
        'username': request.user.username,
        'tipo': request.data.tipo,
        'mensagem': f'Olá, {request.user.username}! Você é {request.user.get_tipo_display()}.'
    })

