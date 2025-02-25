from django.db import models
from django.db.models import Sum
from django.shortcuts import render, redirect
# Create your models here.

class Cliente(models.Model):
    """
    Model para representar um cliente.
    """
    nome = models.CharField(max_length=100, verbose_name="Nome do Cliente")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefone")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço")
    cpfcnpj = models.CharField(max_length=20, blank=False, null=False, verbose_name="CPF/CNPJ")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"




class Produto(models.Model):

    nome = models.CharField(max_length=100, verbose_name="Nome do Produto")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário")

    def __str__(self):
        return f"{self.nome} (R$ {self.preco})"

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('em_andamento', 'Em andamento'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    data_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Data do Pedido")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor Total")

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome}"
    def preco_total(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (R$ {self.preco_total():.2f})"
   

    def save(self, *args, **kwargs):
        # Calcula o valor total somando os valores dos itens do pedido
        self.valor_total = self.itens.aggregate(
            total=Sum(models.F('quantidade') * models.F('preco_unitario'))
        )['total'] or 0
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens', verbose_name="Pedido")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário")

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (R$ {self.preco_unitario})"

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
