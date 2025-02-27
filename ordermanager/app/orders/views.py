from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from .models import Produto, Cliente, ItemPedido, Pedido
from .forms import ClienteForm, ProdutoForm, ItemPedidoFormSet, PedidoForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.
def index(request):
    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()
    itens_pedidos = ItemPedido.objects.all()
    pedidos = Pedido.objects.all()
    return render(request, 'main.html', {
        'clientes': clientes,
        'produtos': produtos,
        'itens_pedidos':itens_pedidos,
        'pedidos': pedidos
    })
    #return  render(request, 'main.html',)



class BuscarProdutosView(View):
    def get(self, request, *args, **kwargs):
        termo = request.GET.get('termo', '')  # Termo de busca
        produtos = Produto.objects.filter(nome__icontains=termo).values('id', 'nome', 'preco')
        return JsonResponse(list(produtos), safe=False)


def cadastar_clientes_form(request):
    # Redireciona para uma página de sucesso
    
    form = ClienteForm()  # Instancia um formulário vazio (para GET)
    # Passa o formulário para o template
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
                # Verifica se o cliente existe
                cliente = Cliente.objects.get(id=cliente_id)
            except Cliente.DoesNotExist:
                messages.error(request, 'Cliente não encontrado.')
                return redirect('main_page')

            try:
                # Cria um único pedido
                pedido = Pedido.objects.create(cliente=cliente)

                # Associa todos os itens ao mesmo pedido
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
                        continue  # Ignora o produto inválido e continua com os demais

                # Atualiza o valor total do pedido
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
        # Processa o formulário do pedido e o FormSet dos itens
        pedido_form = PedidoForm(request.POST, instance=pedido)
        formset = ItemPedidoFormSet(request.POST, instance=pedido)

        if pedido_form.is_valid() and formset.is_valid():
            pedido_form.save()  # Salva o status do pedido
            formset.save()  # Salva os itens do pedido
            pedido.atualizar_valor_total()  # Atualiza o valor total do pedido
            messages.success(request, 'Pedido atualizado com sucesso!')
            return redirect('main_page')
        else:
            messages.error(request, 'Erro ao atualizar o pedido. Verifique os dados.')
    else:
        # Exibe o formulário de edição
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
    # Resumo das Vendas
    total_pedidos = Pedido.objects.count()
    valor_total_faturado = Pedido.objects.aggregate(total=Sum('valor_total'))['total'] or 0
    quantidade_total_produtos = ItemPedido.objects.aggregate(total=Sum('quantidade'))['total'] or 0

    # Pedidos Pendentes
    pedidos_pendentes = Pedido.objects.filter(status='em_andamento')

    # Clientes Mais Ativos
    clientes_mais_ativos = Cliente.objects.annotate(
        total_pedidos=Count('pedido')   
    ).order_by('-total_pedidos')[:10]  # Top 10 clientes

    return render(request, 'relatorios.html', {
        'total_pedidos': total_pedidos,
        'valor_total_faturado': valor_total_faturado,
        'quantidade_total_produtos': quantidade_total_produtos,
        'pedidos_pendentes': pedidos_pendentes,
        'clientes_mais_ativos': clientes_mais_ativos,
    })

