from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Produto, Cliente, ItemPedido, Pedido
from .forms import ClienteForm, ProdutoForm, ItemPedidoFormSet, PedidoForm, RelatorioPedidosForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import csv




# Create your views here.
def index(request):
    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()
    itens_pedidos = ItemPedido.objects.all()
    ultimas_24h = timezone.now() - timedelta(hours=24)
    pedidos = Pedido.objects.filter(data_pedido__gte=ultimas_24h)
    
    return render(request, 'main.html', {
        'clientes': clientes,
        'produtos': produtos,
        'itens_pedidos':itens_pedidos,
        'pedidos': pedidos
    })
  

class BuscarProdutosView(View):
    def get(self, request, *args, **kwargs):
        termo = request.GET.get('termo', '')  # Termo de busca
        produtos = Produto.objects.filter(nome__icontains=termo).values('id', 'nome', 'preco')
        return JsonResponse(list(produtos), safe=False)


def cadastar_clientes_form(request):
    
    
    form = ClienteForm()  

    return render(request, 'cad-clientes.html', {'form': form})

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



def editar_cliente(request, cliente_id):

    cliente = Cliente.objects.get(id=cliente_id)

    if not cliente:
        return redirect('list_clientes') 

    form = ClienteForm(instance=cliente)  

    return render(request, 'editar-cliente.html', {'form': form, 'cliente_id': cliente.id})


def excluir_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    if cliente:
        cliente.delete() 
    return redirect('list_produtos') 

def cadastar_produtos_form(request):

    
    form = ProdutoForm()  
   
    return render(request, 'cad-produtos.html', {'form': form})


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

def listar_clientes(request):
    clientes = Cliente.objects.all()  
    return render(request, 'list-clientes.html', {'clientes': clientes})


def listar_produtos(request):
    produtos = Produto.objects.all()  # Busca todos os clientes no banco de dados
    return render(request, 'list-produtos.html', {'produtos': produtos})


def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)  
    produto.delete()  # Exclui o produto
    return redirect('list_produtos') 



def editar_produto(request, produto_id):

    produto = Produto.objects.get(id=produto_id)

    if not produto:
        return redirect('list_produtos') 

    form = ProdutoForm(instance=produto)  

    return render(request, 'editar-produto.html', {'form': form, 'produto_id': produto.id})




@csrf_exempt
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

def excluir_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)  
    pedido.delete()  
    return redirect('main_page') 


def relatorios(request):
    
    total_pedidos = Pedido.objects.count()
    valor_total_faturado = Pedido.objects.aggregate(total=Sum('valor_total'))['total'] or 0
    quantidade_total_produtos = ItemPedido.objects.aggregate(total=Sum('quantidade'))['total'] or 0

    
    pedidos_pendentes = Pedido.objects.filter(status='em_andamento')

    
    clientes_mais_ativos = Cliente.objects.annotate(
        total_pedidos=Count('pedido')   
    ).order_by('-total_pedidos')[:10] 

    return render(request, 'relatorios.html', {
        'total_pedidos': total_pedidos,
        'valor_total_faturado': valor_total_faturado,
        'quantidade_total_produtos': quantidade_total_produtos,
        'pedidos_pendentes': pedidos_pendentes,
        'clientes_mais_ativos': clientes_mais_ativos,
    })




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

    # Exportar para CSV
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

    # Paginação
    paginator = Paginator(pedidos, 20)  # 20 pedidos por página
    page_number = request.GET.get('page')
    pedidos_paginados = paginator.get_page(page_number)

    return render(request, 'relatorio-pedidos.html', {
        'form': form,
        'pedidos': pedidos_paginados,
    })