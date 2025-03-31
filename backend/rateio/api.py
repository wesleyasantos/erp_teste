from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Usina, UnidadeConsumidora, Rateio, RateioDetalhe, UsinaUC
from .serializers import (
    UsinaSerializer, UnidadeConsumidoraSerializer, 
    RateioSerializer, RateioDetalheSerializer,
    UsinaUCSerializer
)
from .services import CalculadoraRateio

class UsinaViewSet(viewsets.ModelViewSet):
    queryset = Usina.objects.all()
    serializer_class = UsinaSerializer

class UnidadeConsumidoraViewSet(viewsets.ModelViewSet):
    queryset = UnidadeConsumidora.objects.all()
    serializer_class = UnidadeConsumidoraSerializer
    
    @action(detail=True, methods=['get'])
    def usinas(self, request, pk=None):
        uc = self.get_object()
        usinas = UsinaUC.objects.filter(unidade_consumidora=uc)
        serializer = UsinaUCSerializer(usinas, many=True)
        return Response(serializer.data)

class RateioViewSet(viewsets.ModelViewSet):
    queryset = Rateio.objects.all()
    serializer_class = RateioSerializer
    
    @action(detail=False, methods=['post'])
    def calcular(self, request):
        usina_id = request.data.get('usina_id')
        geracao_valor = request.data.get('geracao_valor')
        
        if not usina_id or not geracao_valor:
            return Response(
                {"error": "Forneça usina_id e geracao_valor"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            calculadora = CalculadoraRateio(usina_id, geracao_valor, request.user)
            rateio = calculadora.calcular_rateio()
            
            # Verificar se há necessidade de novas UCs
            detalhes = RateioDetalhe.objects.filter(rateio=rateio)
            total_percentual = sum(d.porcentagem for d in detalhes)
            
            response_data = RateioSerializer(rateio).data
            
            if total_percentual < 95:
                diferenca_kwh = (float(geracao_valor) * (100 - total_percentual)) / 100
                response_data['sugestao'] = {
                    'incluir_novas_ucs': True,
                    'kwh_necessario': round(diferenca_kwh, 2)
                }
                
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def exportar_excel(self, request, pk=None):
        # Implementação da exportação para Excel
        # (Simplificada - você precisará de uma biblioteca como pandas ou xlsxwriter)
        rateio = self.get_object()
        detalhes = RateioDetalhe.objects.filter(rateio=rateio)
        
        # Aqui você geraria o Excel e retornaria como arquivo
        return Response({"message": "Planilha gerada com sucesso"})