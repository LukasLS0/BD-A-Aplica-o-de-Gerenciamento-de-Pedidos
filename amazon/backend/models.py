from django.db import models
from django.utils import choices


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True) # UNIQUE NO BANCO
    telefone = models.CharField(max_length=20, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True) # Preenchido automaticamente
    class Meta:
        db_table = 'clientes' # nome explícito da tabela no banco
        ordering = ['nome'] # Oredenação padrão nas consultas
    
    def __str__(self):
        # Retorna a representação legível do objeto
        return f'{self.nome} <{self.email}>'

class Vendendor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cpf_cpnj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    avaliacao = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vendedores'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.cpf_cpnj})"

class Produto(models.Model):
    
    CATEGORIA_CHOICES = [
        ('eletronicos', 'Eletrônicos'),
        ('roupas',      'Roupas e Acessórios'),
        ('livros',      'Livros'),
        ('alimentos',   'Alimentos'),
        ('outros',      'Outros'),
    ]

    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='outros')
    disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True) # Atualiza a cada save

    class Meta:
        db_table = 'produtos'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"


class Endereco(models.Model):
    ## Precisa fazer choices para o estado? cidade?
    ## cep
    #cliente id
    rua = models.CharField(max_length=255, null=False, blank=False)
    cidade = models.CharField(max_length=100, null=False, blank=False)
    estado = models.CharField(max_length=50, null=False, blank=False)
    cep = models.CharField(max_length=10, null=False, blank=False)

    class Meta:
        db_table = 'enderecos'
        ordering = ['estado']

    def __str__(self):
        return f"{self.rua}, {self.cidade}-{self.estado}"

class FormaPagamento(models.Model):
    ## Precisa fazer o choices para as formas de pagamentos aceitadas
    tipo = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'formas_pagamentos'
        ordering = ['tipo']

    def __str__(self):
        return f"{self.tipo}"

class Item(models.Model):
    # fazer choices de categoria
    # vendedor id
    nome = models.CharField(max_length=100, null=False, blank=False)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    descricao = models.TextField(blank=True)
    categoria = models.CharField(max_length=50, blank=True)
    quantidade_estoque = models.IntegerField(null=False)

    class Meta:
        db_table = 'item'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.categoria}"

class Pedido(models.Model):
    #cliente id
    #endereco id
    #forma pagamento
    data = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'pedidos'
        ordering = ['data']

    def __str__(self):
        return f"{self.data} - {self.status}"

## devo fazer item_pedido?

