from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404
from django.http import JsonResponse
from django.views import View
from .models import Produto, Cliente
from .forms import ClienteForm


# Create your views here.
def index(request):
    return  render(request, 'main.html',)



class BuscarProdutosView(View):
    def get(self, request, *args, **kwargs):
        termo = request.GET.get('termo', '')  # Termo de busca
        produtos = Produto.objects.filter(nome__icontains=termo).values('id', 'nome', 'preco')
        return JsonResponse(list(produtos), safe=False)


def cadastarClientesForm(request):
    # Redireciona para uma página de sucesso
    
    form = ClienteForm()  # Instancia um formulário vazio (para GET)
    # Passa o formulário para o template
    return render(request, 'cad-clientes.html', {'form': form})

def cadastrarClientesSubmit(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)  # Instancia o formulário com os dados enviados
        if form.is_valid():
            form.save()  # Salva o cliente no banco de dados
            return redirect('/cadastrar-cliente')  
        
def listar_clientes(request):
    clientes = Cliente.objects.all()  # Busca todos os clientes no banco de dados
    return render(request, 'list-clientes.html', {'clientes': clientes})

def listar_produtos(request):
    produtos = Produto.objects.all()  # Busca todos os clientes no banco de dados
    return render(request, 'list-produtos.html', {'produtos': produtos})
