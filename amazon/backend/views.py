from contextvars import Token

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Cliente,   Pedido, Vendedor, Produto
from .serializers import ClienteSerializer, PedidoSerializer, UsuarioSerializer, VendedorSerializer, ProdutoSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsVendedor

class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo cliente
    Fornece automaticamente os endpoins list, create, retrieve,
    update, partial update e destroy.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    # Habilita filtros, busca textual e ordenação via query params
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome', 'email'] # ?nome=Maria
    search_fields = ['nome', 'email'] # ?search=Maria
    ordering_fields = ['nome', 'data_cadastro'] # ?ordering=-data_cadastro

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.filter(disponivel=True) # apenas ativos
    serializer_class = ProdutoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsVendedor()]




class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

@api_view(['POST'])
@permission_classes([AllowAny]) # qualquer um vai
def signup(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        usuario = serializer.save()
        token = Token.objects.create(user=usuario)
        return Response({'token': token.key, 'usuario': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([TokenAuthentication])
@permission_classes([IsAuthenticated]) # exige token valido
def perfil(request):
    return Response({
        'username': request.user.username,
        'tipo': request.user.tipo,
        'mensagem': f'Olá, {request.user.username}! Você é {request.user.get_tipo_display()}.'
    })