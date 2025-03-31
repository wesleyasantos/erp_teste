from decimal import Decimal
from .models import Usina, UnidadeConsumidora, Rateio, RateioDetalhe

class CalculadoraRateio:
    def __init__(self, usina_id, geracao_valor, user):
        self.usina = Usina.objects.get(id=usina_id)
        self.geracao = Decimal(geracao_valor)
        self.user = user
        
    def calcular_rateio(self):
        # Criar instância de rateio
        rateio = Rateio.objects.create(
            usina=self.usina,
            geracao_utilizada=self.geracao,
            criado_por=self.user
        )
        
        # Obter todas as UCs vinculadas à usina que não estão marcadas como "não ratear"
        unidades = UnidadeConsumidora.objects.filter(
            usinas__id=self.usina.id, 
            nao_ratear=False
        )
        
        # Calcular proporção de estoque
        for uc in unidades:
            # Usar o maior valor entre consumo médio e último consumo
            consumo = max(uc.consumo_medio, uc.ultimo_consumo)
            
            # Calcular proporção do estoque (meses)
            prop_estoque = Decimal('0')
            if consumo > 0:
                prop_estoque = uc.estoque / consumo
            
            # Definir se deve ratear baseado no grupo da usina
            ratear = True
            if (self.usina.grupo == 'A' and prop_estoque > 3) or \
               (self.usina.grupo == 'B' and prop_estoque > 2):
                ratear = False
            
            # Calcular percentual de rateio inicialmente
            percentual = (consumo / self.geracao * 100) if ratear else Decimal('0.01')
            
            # Definir ação recomendada
            acao = 'MANTER'
            if not ratear:
                acao = 'MANTER'  # Ainda mantém, mas com percentual mínimo
            
            # Criar detalhe do rateio
            RateioDetalhe.objects.create(
                rateio=rateio,
                unidade_consumidora=uc,
                porcentagem=percentual,
                acao=acao,
                estoque_suficiente=not ratear
            )
        
        # Ajustar percentuais para totalizar 100%
        self._ajustar_percentuais(rateio)
        
        return rateio
    
    def _ajustar_percentuais(self, rateio):
        detalhes = RateioDetalhe.objects.filter(rateio=rateio)
        total_percentual = sum(d.porcentagem for d in detalhes)
        
        # Verificar se o total está acima de 100%
        if total_percentual > 100:
            # Sugerir troca de UCs com menor consumo
            detalhes_ordenados = sorted(detalhes, key=lambda x: x.unidade_consumidora.consumo_medio)
            excesso = total_percentual - 100
            
            for detalhe in detalhes_ordenados:
                if excesso <= 0:
                    break
                    
                if detalhe.porcentagem <= excesso:
                    detalhe.acao = 'TROCAR_USINA'
                    excesso -= detalhe.porcentagem
                    detalhe.porcentagem = Decimal('0.01')
                else:
                    detalhe.porcentagem -= excesso
                    excesso = 0
                    
                detalhe.save()
        
        # Recalcular total após ajustes
        detalhes = RateioDetalhe.objects.filter(rateio=rateio)
        total_percentual = sum(d.porcentagem for d in detalhes)
        
        # Ajustar para 100% se estiver entre 95% e 99.9%
        if 95 <= total_percentual < 100:
            # Distribuir a diferença para a UC com maior consumo
            detalhes_ordenados = sorted(
                detalhes, 
                key=lambda x: x.unidade_consumidora.consumo_medio,
                reverse=True
            )
            
            if detalhes_ordenados:
                maior_uc = detalhes_ordenados[0]
                maior_uc.porcentagem += (100 - total_percentual)
                maior_uc.save()
        
        # Se total for menor que 95%, sugerir inclusão de novas UCs
        if total_percentual < 95:
            # O frontend deverá informar ao usuário que novas UCs devem ser incluídas
            diferenca_kwh = (self.geracao * (100 - total_percentual)) / 100
            # Esta informação será retornada ao frontend