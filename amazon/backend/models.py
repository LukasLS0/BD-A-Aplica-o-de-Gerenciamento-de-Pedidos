from django.db import models


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
