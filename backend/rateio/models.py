from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Usina(models.Model):
    nome = models.CharField(max_length=255)
    grupo = models.CharField(max_length=1, choices=[('A', 'Grupo A'), ('B', 'Grupo B')])
    media_transferencia = models.DecimalField(max_digits=10, decimal_places=2)
    dia_faturamento = models.IntegerField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativa = models.BooleanField(default=True)
    
    def total_ucs(self):
        return self.usinauc_set.count()
    
    def __str__(self):
        return f"{self.nome} (Grupo {self.grupo})"
    
    class Meta:
        ordering = ['nome']

class UnidadeConsumidora(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=255)
    consumo_medio = models.DecimalField(max_digits=10, decimal_places=2)
    ultimo_consumo = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nao_faturar = models.BooleanField(default=False)
    nao_ratear = models.BooleanField(default=False)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
    def usinas_vinculadas(self):
        return list(self.usinauc_set.all().values_list('usina__nome', flat=True))
    
    def meses_estoque(self):
        if self.consumo_medio and self.consumo_medio > 0:
            return round(self.estoque / self.consumo_medio, 1)
        return 0
    
    class Meta:
        ordering = ['codigo']

class UsinaUC(models.Model):
    usina = models.ForeignKey(Usina, on_delete=models.CASCADE)
    unidade_consumidora = models.ForeignKey(UnidadeConsumidora, on_delete=models.CASCADE)
    porcentagem_rateio = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    data_vinculacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['usina', 'unidade_consumidora']
        ordering = ['-porcentagem_rateio']

class Rateio(models.Model):
    STATUS_CHOICES = (
        ('RASCUNHO', 'Rascunho'),
        ('FINALIZADO', 'Finalizado'),
        ('APLICADO', 'Aplicado'),
    )
    
    usina = models.ForeignKey(Usina, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    geracao_utilizada = models.DecimalField(max_digits=10, decimal_places=2)
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='RASCUNHO')
    observacoes = models.TextField(blank=True, null=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Rateio de {self.usina.nome} em {self.data_criacao.strftime('%d/%m/%Y')}"
    
    def total_rateado(self):
        return sum(detalhe.porcentagem for detalhe in self.detalhes.all())
    
    class Meta:
        ordering = ['-data_criacao']

class RateioDetalhe(models.Model):
    ACAO_CHOICES = (
        ('MANTER', 'Manter'),
        ('TROCAR_USINA', 'Trocar Usina'),
        ('EXCLUIDO', 'Excluído do Rateio')
    )
    
    rateio = models.ForeignKey(Rateio, on_delete=models.CASCADE, related_name='detalhes')
    unidade_consumidora = models.ForeignKey(UnidadeConsumidora, on_delete=models.CASCADE)
    porcentagem = models.DecimalField(max_digits=5, decimal_places=2)
    estoque_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    acao = models.CharField(max_length=20, choices=ACAO_CHOICES, default='MANTER')
    estoque_suficiente = models.BooleanField(default=False)
    meses_calculados = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def kwh_rateado(self):
        return (self.rateio.geracao_utilizada * self.porcentagem) / Decimal('100.0')
    
    class Meta:
        unique_together = ['rateio', 'unidade_consumidora']