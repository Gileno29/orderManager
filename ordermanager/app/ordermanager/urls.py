"""
URL configuration for ordermanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from orders import views as orderviews
from orders import views_api as apiview
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', orderviews.index, name='main_page' ),
    path('buscar-produtos/', orderviews.BuscarProdutosView.as_view(), name='buscar_produtos'),
    path('cadastrar-cliente/', orderviews.cadastar_clientes_form, name='cadastrar_cliente'),
    path('cadastrar-cliente/submit/', orderviews.cadastrar_clientes_submit, name='cadastrar_submicao'),
    path('cadastrar-cliente/submit/<int:cliente_id>/', orderviews.cadastrar_clientes_submit, name='editar_submicao'),
    path('editar-cliente/<int:cliente_id>/', orderviews.editar_cliente, name='editar_cliente'),
    path('excluir-cliente/<int:cliente_id>/', orderviews.excluir_cliente, name='excluir_cliente'),
    path('list-clientes/', orderviews.listar_clientes, name='list_clientes'),
    path('list-produtos/', orderviews.listar_produtos, name='list_produtos'),
    path('cadastrar-produtos/', orderviews.cadastar_produtos_form, name='cadastrar_produto'),
    path('cadastrar-produtos/submit/', orderviews.cadastrar_produtos_submit, name='cadastrar_submicao_produtos'),
    path('cadastrar-produtos/submit/<int:produto_id>', orderviews.cadastrar_produtos_submit, name='editar_submicao_produtos'),
    path('excluir-produto/<int:produto_id>/', orderviews.excluir_produto, name='excluir_produto'),
    path('editar-produto/<int:produto_id>/', orderviews.editar_produto, name='editar_produto'),
    path('salvar-pedido/', orderviews.salvar_pedido, name='salvar_pedido'),
    path('editar-pedido/<int:pedido_id>/editar/', orderviews.editar_pedido, name='editar_pedido'),
    path('excluir-pedido/<int:pedido_id>/', orderviews.excluir_pedido, name='excluir_pedido'),
    path('relatorios/', orderviews.relatorios, name='relatorios'),
    path('api/encontrar-vogal/', apiview.EncontrarVogalView.as_view(), name='encontrar_vogal'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
