from django import forms 
from .models import Cliente, Produto, ItemPedido, Pedido
from django.forms import inlineformset_factory

class ClienteForm(forms.ModelForm):
    class Meta:
        model= Cliente
        fields = ['nome', 'email', 'telefone', 'endereco', 'cpfcnpj']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cpfcnpj': forms.TextInput(attrs={'class': 'form-control'})
        }


class ProdutoForm(forms.ModelForm):
    class Meta:
        model= Produto
        fields = ['nome', 'descricao', 'preco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
        }
ItemPedidoFormSet = inlineformset_factory(
    Pedido,  # Modelo pai
    ItemPedido,  # Modelo filho
    fields=('produto', 'quantidade'),  # Campos que podem ser editados
    extra=1,  # Número de formulários extras em branco
    can_delete=True,  # Permite excluir itens
)