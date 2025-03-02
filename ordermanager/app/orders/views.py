from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Produto, Cliente, ItemPedido, Pedido
from .forms import ClienteForm, ProdutoForm, ItemPedidoFormSet, PedidoForm, RelatorioPedidosForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import csv
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User




# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'login.html'  
    redirect_authenticated_user = True  
    success_url = reverse_lazy('main_page')  



@csrf_exempt
@login_required
def index(request):
    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()
    itens_pedidos = ItemPedido.objects.all()
    ultimas_24h = timezone.now() - timedelta(hours=24)
    pedidos = Pedido.objects.filter(data_pedido__gte=ultimas_24h).order_by('-data_pedido')
    
    paginator = Paginator(pedidos, 8)
    page_number = request.GET.get('page')  
    pedidos_paginados = paginator.get_page(page_number)  
    return render(request, 'main.html', {
        'clientes': clientes,
        'produtos': produtos,
        'itens_pedidos':itens_pedidos,
        'pedidos': pedidos_paginados
    })
  

@login_required
def cadastar_clientes_form(request):
    
    
    form = ClienteForm()  

    return render(request, 'cad-clientes.html', {'form': form})

@login_required
def cadastrar_clientes_submit(request, cliente_id=None):
    if request.method == 'POST':
        if cliente_id:
            cliente= Cliente.objects.get(id=cliente_id)
            form = ClienteForm(request.POST, instance=cliente)
        else:
            form = ClienteForm(request.POST)  
        if form.is_valid():
            form.save()  
            return redirect('/list-clientes')


@login_required
def editar_cliente(request, cliente_id):

    cliente = Cliente.objects.get(id=cliente_id)

    if not cliente:
        return redirect('list_clientes') 

    form = ClienteForm(instance=cliente)  

    return render(request, 'editar-cliente.html', {'form': form, 'cliente_id': cliente.id})

@login_required
def excluir_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    if cliente:
        cliente.delete() 
    return redirect('list_produtos') 

@login_required
def cadastar_produtos_form(request):

    
    form = ProdutoForm()  
   
    return render(request, 'cad-produtos.html', {'form': form})

@login_required
def cadastrar_produtos_submit(request, produto_id=None):
    if request.method == 'POST':
        if produto_id:
            produto = get_object_or_404(Produto, id=produto_id)  
            form = ProdutoForm(request.POST, instance=produto)
        
        else:
            form = ProdutoForm(request.POST)  
        if form.is_valid():
            form.save()  
            return redirect('/list-produtos') 
@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()  
    return render(request, 'list-clientes.html', {'clientes': clientes})

@login_required
def listar_produtos(request):
    produtos = Produto.objects.all()  # Busca todos os clientes no banco de dados
    return render(request, 'list-produtos.html', {'produtos': produtos})

@login_required
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)  
    produto.delete()  # Exclui o produto
    return redirect('list_produtos') 


@login_required
def editar_produto(request, produto_id):

    produto = Produto.objects.get(id=produto_id)

    if not produto:
        return redirect('list_produtos') 

    form = ProdutoForm(instance=produto)  

    return render(request, 'editar-produto.html', {'form': form, 'produto_id': produto.id})




@csrf_exempt
@login_required
def salvar_pedido(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        produtos = request.POST.getlist('produtos[]')
        quantidades = request.POST.getlist('quantidades[]')

        if cliente_id and produtos and quantidades:
            try:
                
                cliente = Cliente.objects.get(id=cliente_id)
            except Cliente.DoesNotExist:
                messages.error(request, 'Cliente não encontrado.')
                return redirect('main_page')

            try:
                
                pedido = Pedido.objects.create(cliente=cliente)

               
                for produto_id, quantidade in zip(produtos, quantidades):
                    try:
                        produto = Produto.objects.get(id=produto_id)
                        ItemPedido.objects.create(
                            pedido=pedido,
                            produto=produto,
                            quantidade=quantidade
                        )
                    except Produto.DoesNotExist:
                        messages.error(request, f'Produto com ID {produto_id} não encontrado.')
                        continue 

               
                pedido.atualizar_valor_total()

                messages.success(request, 'Pedido salvo com sucesso!')
                return redirect('main_page')
            except Exception as e:
                messages.error(request, f'Erro ao salvar o pedido: {str(e)}')
        else:
            messages.error(request, 'Dados inválidos. Preencha todos os campos.')
    else:
        messages.error(request, 'Método de requisição inválido.')

    return render(request, 'main.html', {
        'clientes': Cliente.objects.all(),
        'produtos': Produto.objects.all(),
    })


@login_required
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        
        pedido_form = PedidoForm(request.POST, instance=pedido)
        formset = ItemPedidoFormSet(request.POST, instance=pedido)

        if pedido_form.is_valid() and formset.is_valid():
            pedido_form.save()  
            formset.save() 
            pedido.atualizar_valor_total()  
            messages.success(request, 'Pedido atualizado com sucesso!')
            return redirect('main_page')
        else:
            messages.error(request, 'Erro ao atualizar o pedido. Verifique os dados.')
    else:
        
        pedido_form = PedidoForm(instance=pedido)
        formset = ItemPedidoFormSet(instance=pedido)

    return render(request, 'editar-pedido.html', {
        'pedido': pedido,
        'pedido_form': pedido_form,
        'formset': formset,
    })

@login_required
def excluir_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)  
    pedido.delete()  
    return redirect('main_page') 

@login_required
def relatorios(request):
    
    total_pedidos = Pedido.objects.count()
    valor_total_faturado = Pedido.objects.filter(status='finalizado').aggregate(total=Sum('valor_total'))['total'] or 0
    quantidade_total_produtos = ItemPedido.objects.filter(pedido__status='finalizado').aggregate(total=Sum('quantidade'))['total'] or 0

    
    pedidos_pendentes = Pedido.objects.filter(status='em_andamento')

    
    clientes_mais_ativos = Cliente.objects.annotate(
        total_pedidos=Count('pedido')   
    ).order_by('-total_pedidos')[:10] 
    paginator = Paginator(pedidos_pendentes, 10)  
    page_number = request.GET.get('page')  
    pedidos_paginados = paginator.get_page(page_number) 
    

    return render(request, 'relatorios.html', {
        'total_pedidos': total_pedidos,
        'valor_total_faturado': valor_total_faturado,
        'quantidade_total_produtos': quantidade_total_produtos,
        'pedidos_pendentes': pedidos_paginados,
        'clientes_mais_ativos': clientes_mais_ativos,
    })



@login_required
def relatorio_pedidos(request):
    form = RelatorioPedidosForm(request.GET or None)
    pedidos = Pedido.objects.all()

    if form.is_valid():
        data_inicial = form.cleaned_data.get('data_inicial')
        data_final = form.cleaned_data.get('data_final')
        status = form.cleaned_data.get('status')
        cliente = form.cleaned_data.get('cliente')
        produto = form.cleaned_data.get('produto')
        valor_minimo = form.cleaned_data.get('valor_minimo')
        quantidade_itens = form.cleaned_data.get('quantidade_itens')

        # Aplicar filtros
        if data_inicial:
            pedidos = pedidos.filter(data_pedido__gte=data_inicial)
        if data_final:
            pedidos = pedidos.filter(data_pedido__lte=data_final)
        if status:
            pedidos = pedidos.filter(status=status)
        if cliente:
            pedidos = pedidos.filter(cliente=cliente)
        if produto:
            pedidos = pedidos.filter(itens__produto=produto).distinct()
        if valor_minimo:
            pedidos = pedidos.filter(valor_total__gte=valor_minimo)
        if quantidade_itens:
            pedidos = pedidos.annotate(num_itens=Count('itens')).filter(num_itens__gte=quantidade_itens)

    # Ordenação
    ordenacao = request.GET.get('ordenacao', 'data_pedido')
    pedidos = pedidos.order_by(ordenacao)

   
    if 'exportar_csv' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_pedidos.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Cliente', 'Data', 'Status', 'Valor Total', 'Quantidade de Itens'])

        for pedido in pedidos:
            writer.writerow([
                pedido.id,
                pedido.cliente.nome,
                pedido.data_pedido.strftime('%d/%m/%Y %H:%M'),
                pedido.get_status_display(),
                pedido.valor_total,
                pedido.itens.count()
            ])

        return response

   
    paginator = Paginator(pedidos, 20)  
    page_number = request.GET.get('page')
    pedidos_paginados = paginator.get_page(page_number)

    return render(request, 'relatorio-pedidos.html', {
        'form': form,
        'pedidos': pedidos_paginados,
    })


@login_required
def criar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Nome de usuário já existe.')
            else:
                
                User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Usuário criado com sucesso!')
                return redirect('list_usuarios')  
        else:
            messages.error(request, 'As senhas não coincidem.')
    return render(request, 'criar-usuario.html')

@login_required
def listar_usuarios(request):
    usuarios = User.objects.all()  
    return render(request, 'list-usuarios.html', {'usuarios': usuarios})


@csrf_exempt
@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)  # Obtém o usuário ou retorna 404
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            usuario.username = username
            usuario.email = email
            if password:  
                usuario.set_password(password)
            usuario.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('list_usuarios')
        else:
            messages.error(request, 'As senhas não coincidem.')
    return render(request, 'editar-usuario.html', {'usuario': usuario})

@login_required
def deletar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id) 
    if request.method == 'POST':
        usuario.delete()  
        messages.success(request, 'Usuário deletado com sucesso!')
    return redirect('list_usuarios')


def exportar_pedidos_pendentes_csv(request):
    # Filtra os pedidos pendentes
    pedidos_pendentes = Pedido.objects.filter(status='em_andamento')

    # Cria a resposta HTTP com o tipo de conteúdo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pedidos_pendentes.csv"'

    # Cria o escritor CSV
    writer = csv.writer(response)
    writer.writerow(['ID', 'Cliente', 'Valor Total', 'Data do Pedido'])  # Cabeçalho

    # Escreve os dados dos pedidos
    for pedido in pedidos_pendentes:
        writer.writerow([
            pedido.id,
            pedido.cliente.nome,
            pedido.valor_total,
            pedido.data_pedido.strftime('%d/%m/%Y %H:%M'),
        ])

    return response

def exportar_clientes_ativos_csv(request):
    
    clientes_mais_ativos = Cliente.objects.annotate(total_pedidos=Count('pedido')).order_by('-total_pedidos')

 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clientes_mais_ativos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Cliente', 'Total de Pedidos', 'cpfcnpj'])  

    
    for cliente in clientes_mais_ativos:
        writer.writerow([
            cliente.nome,
            cliente.total_pedidos,
            cliente.cpfcnpj
        ])

    return response