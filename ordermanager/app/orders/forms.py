from django import forms 
from .models import Cliente, Produto
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
            'descricao': forms.EmailInput(attrs={'class': 'form-control'}),
            'preco': forms.TextInput(attrs={'class': 'form-control'}),
        }
