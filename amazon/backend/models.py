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


