from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend import views

router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet, basename='cliente')
router.register(r'vendedores', views.VendedorViewSet, basename='vendedor')
router.register(r'produtos', views.ProdutoViewSet, basename='produto')
router.register(r'enderecos', views.EnderecoViewSet, basename='endereco')
router.register(r'formaspagamento', views.FormaPagamentoViewSet, basename='formapagamento')
router.register(r'itens', views.ItemViewSet, basename='item')
router.register(r'pedidos', views.PedidoViewSet, basename='pedido')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("amazon_api/", include(router.urls)) # Todos os endpoints da API
]


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view (
    openapi.Info(
        title ='Amazon API',
        default_version='v1',
        description='API RESTful para gerenciamento de pedidos',
        contact=openapi.Contact(email='contato@amazon.com'),
        license=openapi.License(name='MIT License')
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
]
