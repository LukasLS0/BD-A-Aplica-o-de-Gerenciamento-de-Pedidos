from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Cliente, Endereco, Item, Pedido, Vendendor, Produto
from .serializers import ClienteSerializer, EnderecoSerializer, FormaPagamentoSerializer, ItemSerializer, PedidoSerializer, VendedorSerializer, ProdutoSerializer


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
    queryset = Vendendor.objects.all()
    serializer_class = VendedorSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.filter(disponivel=True) # apenas ativos
    serializer_class = ProdutoSerializer

class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

class FormaPagamentoViewSet(viewsets.ModelViewSet):
    queryset = FormaPagamento.objects.all()
    serializer_class = FormaPagamentoSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

