<!-- src/views/rateio/RateioView.vue -->
<template>
  <div class="rateio-container">
    <!-- Header Card -->
    <div class="card mb-3">
      <div class="flex flex-column md:flex-row md:align-items-center md:justify-content-between">
        <div class="mb-3 md:mb-0">
          <h2 class="mb-1 text-xl font-medium">Cálculo de Rateio</h2>
          <p class="text-600 m-0">Configure os parâmetros e calcule a distribuição de energia</p>
        </div>
        <div>
          <Button 
            v-if="resultadoRateio && resultadoRateio.id"
            label="Histórico" 
            icon="pi pi-history" 
            text
            @click="$router.push('/historico-rateio')"
            class="mr-2"
          />
          <Button 
            v-if="resultadoRateio && resultadoRateio.id"
            label="Exportar Excel" 
            icon="pi pi-file-excel" 
            severity="success"
            @click="exportarExcel"
            :disabled="resultadoRateio.status !== 'FINALIZADO'"
          />
        </div>
      </div>
    </div>
    
    <!-- Configuration Card -->
    <div class="card mb-3">
      <h3 class="mb-3">Parâmetros de Rateio</h3>
      
      <div class="grid">
        <div class="col-12 md:col-6 lg:col-4">
          <div class="field">
            <label for="usina" class="font-medium mb-2 block">Selecione a Usina</label>
            <Dropdown 
              id="usina" 
              v-model="selectedUsina" 
              :options="usinas" 
              optionLabel="nome" 
              placeholder="Selecione uma usina"
              class="w-full"
              :filter="true"
              :loading="loading.usinas"
              @change="carregarInformacoesUsina" 
            >
              <template #value="slotProps">
                <div v-if="slotProps.value" class="flex align-items-center">
                  <i class="pi pi-bolt mr-2"></i>
                  <div>{{ slotProps.value.nome }}</div>
                </div>
                <span v-else>Selecione uma usina</span>
              </template>
              <template #option="slotProps">
                <div class="flex align-items-center">
                  <i class="pi pi-bolt mr-2"></i>
                  <div>
                    <div>{{ slotProps.option.nome }}</div>
                    <small class="text-600">Grupo {{ slotProps.option.grupo }} · {{ slotProps.option.media_transferencia }} kWh</small>
                  </div>
                </div>
              </template>
            </Dropdown>
          </div>
        </div>
        
        <div class="col-12 md:col-6 lg:col-4" v-if="selectedUsina">
          <div class="field">
            <label for="geracao" class="font-medium mb-2 block">Geração para Rateio (kWh)</label>
            <div class="p-inputgroup">
              <InputNumber 
                id="geracao" 
                v-model="geracaoValor" 
                :min="0" 
                mode="decimal" 
                :maxFractionDigits="2"
                placeholder="Valor em kWh"
                class="w-full"
              />
              <Button 
                icon="pi pi-refresh" 
                @click="usarMediaGeracao" 
                severity="secondary"
                v-tooltip.top="'Usar média da usina'"
              />
            </div>
            <small v-if="selectedUsina" class="text-600 block mt-1">
              Média histórica: {{ selectedUsina.media_transferencia }} kWh
            </small>
          </div>
        </div>
        
        <div class="col-12 md:col-6 lg:col-4" v-if="selectedUsina">
          <div class="field">
            <label class="font-medium mb-2 block">Ação</label>
            <Button 
              label="Calcular Rateio" 
              icon="pi pi-calculator" 
              severity="primary" 
              class="w-full p-button-raised" 
              @click="calcularRateio"
              :loading="loading.calculo"
              :disabled="!geracaoValor || geracaoValor <= 0"
            />
            <small class="text-600 block mt-1">
              O cálculo seguirá regras para usinas do Grupo {{ selectedUsina.grupo }}
            </small>
          </div>
        </div>
      </div>
      
      <!-- Usina Info -->
      <div class="mt-3 p-3 border-1 surface-border border-round" v-if="selectedUsina">
        <div class="flex flex-column md:flex-row md:align-items-center">
          <div class="flex-1">
            <h4 class="mb-1 mt-0">{{ selectedUsina.nome }}</h4>
            <div class="flex align-items-center text-600">
              <i class="pi pi-tag mr-2"></i>
              <span>Grupo {{ selectedUsina.grupo }}</span>
              <i class="pi pi-calendar ml-3 mr-2"></i>
              <span>Faturamento dia {{ selectedUsina.dia_faturamento }}</span>
              <i class="pi pi-users ml-3 mr-2"></i>
              <span>{{ selectedUsina.total_ucs }} UCs vinculadas</span>
            </div>
          </div>
          <div class="mt-3 md:mt-0">
            <Tag 
              :severity="selectedUsina.grupo === 'A' ? 'info' : 'success'" 
              :value="'Grupo ' + selectedUsina.grupo"
              class="mr-2"
            />
            <Button 
              label="Ver UCs" 
              icon="pi pi-list"
              text
              @click="verUCs(selectedUsina.id)"
            />
          </div>
        </div>
      </div>
    </div>
    
    <!-- Results Section -->
    <div class="card" v-if="resultadoRateio && resultadoRateio.detalhes">
      <div class="flex justify-content-between align-items-center mb-4">
        <h3 class="m-0">Resultado do Rateio</h3>
        <div>
          <Tag 
            :severity="getBadgeSeverity()" 
            :value="getStatusLabel()"
          />
        </div>
      </div>
      
      <!-- Results Summary -->
      <div class="grid mb-4">
        <div class="col-12 md:col-4">
          <div class="p-3 border-round bg-primary-50">
            <div class="flex align-items-center">
              <i class="pi pi-bolt text-primary-600 text-3xl mr-3"></i>
              <div>
                <div class="text-sm text-primary-600 mb-1">Geração Total</div>
                <div class="text-xl font-medium">{{ formatNumber(resultadoRateio.geracao_utilizada) }} kWh</div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-12 md:col-4">
      <div class="p-3 border-round" :class="totalRateio === 100 ? 'bg-success-50' : 'bg-warning-50'">
        <div class="flex align-items-center">
          <i class="pi" :class="[totalRateio === 100 ? 'pi-check-circle text-success-600' : 'pi-exclamation-triangle text-warning-600', 'text-3xl mr-3']"></i>
          <div>
            <div class="text-sm" :class="totalRateio === 100 ? 'text-success-600' : 'text-warning-600'">Status</div>
            <div class="text-xl font-medium">{{ totalRateio === 100 ? 'Rateio Válido' : 'Ajuste Necessário' }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Tabela de Resultados -->
  <DataTable 
    :value="resultadoRateio.detalhes" 
    :paginator="true"
    :rows="10"
    :rowsPerPageOptions="[10, 25, 50]"
    responsiveLayout="scroll"
    stripedRows
    class="p-datatable-sm"
    v-model:filters="filters"
    filterDisplay="menu"
    :loading="loading.tabela"
  >
    <Column field="unidade_consumidora.codigo" header="Código UC" :sortable="true" filterMatchMode="contains">
      <template #filter="{ filterModel, filterCallback }">
        <InputText v-model="filterModel.value" @input="filterCallback()" placeholder="Buscar por código" />
      </template>
    </Column>
    
    <Column field="unidade_consumidora.nome" header="Nome UC" :sortable="true" filterMatchMode="contains">
      <template #filter="{ filterModel, filterCallback }">
        <InputText v-model="filterModel.value" @input="filterCallback()" placeholder="Buscar por nome" />
      </template>
    </Column>
    
    <Column field="unidade_consumidora.consumo_medio" header="Consumo (kWh)" :sortable="true">
      <template #body="slotProps">
        {{ formatNumber(slotProps.data.unidade_consumidora.consumo_medio) }}
      </template>
    </Column>
    
    <Column field="estoque_anterior" header="Estoque (kWh)" :sortable="true">
      <template #body="slotProps">
        {{ formatNumber(slotProps.data.estoque_anterior) }}
      </template>
    </Column>
    
    <Column field="meses_calculados" header="Meses Estoque" :sortable="true">
      <template #body="slotProps">
        <Tag :severity="getMesesSeverity(slotProps.data.meses_calculados)">
          {{ slotProps.data.meses_calculados.toFixed(1) }}
        </Tag>
      </template>
    </Column>
    
    <Column field="porcentagem" header="% Rateio" :sortable="true">
      <template #body="slotProps">
        <div class="p-inputgroup">
          <InputNumber 
            v-model="slotProps.data.porcentagem" 
            :min="0.01" 
            :max="100" 
            :step="0.01"
            mode="decimal" 
            :maxFractionDigits="2"
            :disabled="resultadoRateio.status !== 'RASCUNHO' || slotProps.data.estoque_suficiente"
            class="w-12rem"
            @change="atualizarTotalRateio"
          />
          <span class="p-inputgroup-addon">%</span>
        </div>
      </template>
    </Column>
    
    <Column field="kwh_rateado" header="kWh Rateado" :sortable="true">
      <template #body="slotProps">
        {{ formatNumber(calcularKwhRateado(slotProps.data.porcentagem)) }}
      </template>
    </Column>
    
    <Column field="acao" header="Ação Sugerida" :sortable="true">
      <template #body="slotProps">
        <Tag :severity="getAcaoSeverity(slotProps.data.acao)">
          {{ formatarAcao(slotProps.data.acao) }}
        </Tag>
      </template>
      <template #filter="{ filterModel, filterCallback }">
        <Dropdown 
          v-model="filterModel.value" 
          @change="filterCallback()"
          :options="acoesOptions" 
          optionLabel="label" 
          optionValue="value"
          placeholder="Selecionar ação" 
          class="p-column-filter"
          showClear
        />
      </template>
    </Column>
    
    <Column field="estoque_suficiente" header="Estoque" :sortable="true">
      <template #body="slotProps">
        <i 
          :class="slotProps.data.estoque_suficiente ? 
            'pi pi-check-circle text-success-500 text-xl' : 'pi pi-times-circle text-danger-500 text-xl'"
          v-tooltip.top="slotProps.data.estoque_suficiente ? 'Estoque suficiente' : 'Estoque insuficiente'"
        ></i>
      </template>
      <template #filter="{ filterModel, filterCallback }">
        <TriStateCheckbox v-model="filterModel.value" @change="filterCallback()" />
      </template>
    </Column>
  </DataTable>
  
  <!-- Controles de Rateio -->
  <div class="flex flex-column md:flex-row md:justify-content-between md:align-items-center p-3 mt-4 border-round surface-50">
    <div class="mb-3 md:mb-0">
      <div class="text-xl font-medium mb-2">
        Total: {{ totalRateio.toFixed(2) }}%
        <Tag 
          :severity="totalRateio === 100 ? 'success' : 'danger'"
          class="ml-2"
        >
          {{ totalRateio === 100 ? 'Válido' : 'Ajuste Necessário' }}
        </Tag>
      </div>
      
      <div v-if="totalRateio !== 100">
        <small class="text-600">
          {{ totalRateio > 100 ? 
            `O total excede 100% em ${(totalRateio - 100).toFixed(2)}%. Reduza o percentual de algumas UCs.` : 
            `Faltam ${(100 - totalRateio).toFixed(2)}% para completar o rateio.` }}
        </small>
      </div>
    </div>
    
    <div class="flex flex-column sm:flex-row gap-2">
      <Button 
        label="Auto Ajustar" 
        icon="pi pi-sliders-h" 
        severity="secondary" 
        @click="autoAjustarRateio"
        :disabled="totalRateio === 100 || resultadoRateio.status !== 'RASCUNHO'"
        v-tooltip.top="'Ajustar automaticamente para totalizar 100%'"
      />
      <Button 
        label="Finalizar Rateio" 
        icon="pi pi-check" 
        severity="success" 
        @click="finalizarRateio"
        :disabled="totalRateio !== 100 || resultadoRateio.status !== 'RASCUNHO'"
      />
    </div>
  </div>
  
  <!-- Mensagens e Alertas -->
  <Message 
    v-if="resultadoRateio.sugestao && resultadoRateio.sugestao.incluir_novas_ucs" 
    severity="warn" 
    class="mt-4"
  >
    <template #icon>
      <i class="pi pi-exclamation-triangle text-2xl"></i>
    </template>
    <div class="ml-2">
      <h4 class="m-0 p-0 mb-1">Novas UCs Necessárias</h4>
      <p class="m-0 p-0">
        É recomendado incluir novas Unidades Consumidoras para atingir um rateio mais eficiente.
        <strong>kWh necessário para inclusão:</strong> 
        {{ formatNumber(resultadoRateio.sugestao.kwh_necessario) }}
      </p>
      <div class="mt-2">
        <Button 
          label="Gerenciar UCs" 
          icon="pi pi-plus-circle" 
          size="small" 
          text
          @click="$router.push('/unidades-consumidoras')"
        />
      </div>
    </div>
  </Message>
</div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const toast = useToast();
const confirm = useConfirm();

// Estado
const usinas = ref([]);
const selectedUsina = ref(null);
const geracaoValor = ref(null);
const resultadoRateio = ref(null);
const loading = ref({
  usinas: false,
  calculo: false,
  tabela: false,
  finalizacao: false
});

// Filtros da tabela
const filters = ref({
  'unidade_consumidora.codigo': { value: null, matchMode: 'contains' },
  'unidade_consumidora.nome': { value: null, matchMode: 'contains' },
  'acao': { value: null, matchMode: 'equals' },
  'estoque_suficiente': { value: null, matchMode: 'equals' }
});

// Opções para filtro de ações
const acoesOptions = ref([
  { label: 'Manter', value: 'MANTER' },
  { label: 'Trocar Usina', value: 'TROCAR_USINA' },
  { label: 'Excluído', value: 'EXCLUIDO' }
]);

// Computed props
const totalRateio = computed(() => {
  if (!resultadoRateio.value || !resultadoRateio.value.detalhes) return 0;
  
  return resultadoRateio.value.detalhes.reduce(
    (total, detalhe) => total + Number(detalhe.porcentagem), 
    0
  );
});

// Methods
function formatNumber(value) {
  if (!value && value !== 0) return '';
  return new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 2 }).format(value);
}

async function carregarUsinas() {
  loading.value.usinas = true;
  try {
    // Demo: Simular chamada de API com dados pré-definidos
    // Em produção, seria: const response = await axios.get('/api/rateio/usinas/');
    await new Promise(resolve => setTimeout(resolve, 500)); // Simulação de delay
    
    usinas.value = [
      { id: 1, nome: 'Usina Solar Horizonte', grupo: 'A', media_transferencia: 15000, dia_faturamento: 10, total_ucs: 8 },
      { id: 2, nome: 'Usina Eólica Norte', grupo: 'B', media_transferencia: 8500, dia_faturamento: 15, total_ucs: 12 },
      { id: 3, nome: 'Usina Solar Meridional', grupo: 'A', media_transferencia: 22000, dia_faturamento: 5, total_ucs: 15 },
      { id: 4, nome: 'Usina Fotovoltaica Central', grupo: 'B', media_transferencia: 7200, dia_faturamento: 20, total_ucs: 6 }
    ];
    
    // Verificar se há usina na rota
    if (route.query.usina) {
      const usinaId = parseInt(route.query.usina);
      selectedUsina.value = usinas.value.find(u => u.id === usinaId);
      if (selectedUsina.value) {
        await carregarInformacoesUsina();
      }
    }
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Erro',
      detail: 'Falha ao carregar usinas',
      life: 3000
    });
  } finally {
    loading.value.usinas = false;
  }
}

function carregarInformacoesUsina() {
  if (!selectedUsina.value) return;
  
  // Usar a média de geração como valor padrão
  geracaoValor.value = selectedUsina.value.media_transferencia;
}

function usarMediaGeracao() {
  if (selectedUsina.value) {
    geracaoValor.value = selectedUsina.value.media_transferencia;
  }
}

async function calcularRateio() {
  if (!selectedUsina.value || !geracaoValor.value) {
    toast.add({
      severity: 'warn',
      summary: 'Atenção',
      detail: 'Selecione uma usina e informe o valor de geração',
      life: 3000
    });
    return;
  }
  
  loading.value.calculo = true;
  
  try {
    // Demo: Simular chamada de API com dados pré-definidos
    // Em produção, seria: const response = await axios.post('/api/rateio/calcular/', {...});
    await new Promise(resolve => setTimeout(resolve, 800)); // Simulação de delay
    
    // Gerar dados de demonstração com base na usina e geração
    resultadoRateio.value = gerarDemonstracaoRateio(selectedUsina.value, geracaoValor.value);
    
    toast.add({
      severity: 'success',
      summary: 'Rateio Calculado',
      detail: 'O rateio foi calculado com sucesso',
      life: 3000
    });
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Erro',
      detail: 'Falha ao calcular o rateio',
      life: 3000
    });
  } finally {
    loading.value.calculo = false;
  }
}

// Função para gerar dados de demonstração
function gerarDemonstracaoRateio(usina, geracao) {
  const id = Math.floor(Math.random() * 1000) + 1;
  const dataHoje = new Date();
  
  // Gerar UCs conforme as regras do documento
  const detalhes = [];
  const totalUCs = usina.total_ucs;
  let totalAlocado = 0;
  
  for (let i = 0; i < totalUCs; i++) {
    const codigo = `UC${100000 + i}`;
    const nome = `Unidade Consumidora ${i+1}`;
    
    // Definir consumo médio e estoque de forma a criar alguns casos interessantes
    let consumo = (Math.random() * 0.2 + 0.05) * geracao; // Entre 5% e 25% da geração
    consumo = parseFloat(consumo.toFixed(2));
    
    // Alguns casos terão estoque alto para demonstrar regras de estoque suficiente
    let estoque = i % 3 === 0 ? 
      consumo * (usina.grupo === 'A' ? 4 : 3) : // Estoque alto 
      consumo * Math.random(); // Estoque baixo
    estoque = parseFloat(estoque.toFixed(2));
    
    // Calcular meses de estoque
    const mesesEstoque = parseFloat((estoque / consumo).toFixed(2));
    
    // Determinar se deve ratear com base nas regras
    const estoqueSuficiente = (usina.grupo === 'A' && mesesEstoque > 3) || 
                              (usina.grupo === 'B' && mesesEstoque > 2);
    
    // Definir percentual
    let percentual;
    if (estoqueSuficiente) {
      percentual = 0.01; // Percentual mínimo
    } else {
      percentual = parseFloat(((consumo / geracao) * 100).toFixed(2));
      // Limitar a um valor razoável para demonstração
      if (percentual > 35) percentual = 35;
    }
    
    // Acumular para não ultrapassar 100%
    totalAlocado += percentual;
    if (totalAlocado > 100 && i < totalUCs - 1) {
      // Reduzir este percentual para não ultrapassar
      percentual = Math.max(0.01, percentual - (totalAlocado - 100) - 0.01);
      totalAlocado = percentual + (totalAlocado - percentual);
    } else if (i === totalUCs - 1 && totalAlocado < 100) {
      // Último item, ajustar para chegar a 100%
      percentual = 100 - (totalAlocado - percentual);
    }
    
    // Definir ação sugerida
    let acao = 'MANTER';
    if (estoqueSuficiente) {
      acao = 'MANTER'; // Manter com percentual mínimo
    } else if (i === totalUCs - 1 && totalAlocado > 100) {
      acao = 'TROCAR_USINA'; // Sugerir troca para último item se ultrapassar 100%
    }
    
    detalhes.push({
      id: i + 1,
      rateio_id: id,
      unidade_consumidora: {
        id: i + 1,
        codigo: codigo,
        nome: nome,
        consumo_medio: consumo,
        ultimo_consumo: consumo * (0.9 + Math.random() * 0.2)
      },
      estoque_anterior: estoque,
      porcentagem: percentual,
      acao: acao,
      estoque_suficiente: estoqueSuficiente,
      meses_calculados: mesesEstoque
    });
  }
  
  // Criar objeto rateio
  return {
    id: id,
    usina: usina,
    geracao_utilizada: geracao,
    data_criacao: dataHoje.toISOString(),
    criado_por: { id: 1, username: 'admin' },
    status: 'RASCUNHO',
    detalhes: detalhes,
    sugestao: totalAlocado < 95 ? {
      incluir_novas_ucs: true,
      kwh_necessario: parseFloat((geracao * (100 - totalAlocado) / 100).toFixed(2))
    } : null
  };
}

function calcularKwhRateado(percentual) {
  if (!resultadoRateio.value || !resultadoRateio.value.geracao_utilizada) return 0;
  return (resultadoRateio.value.geracao_utilizada * percentual) / 100;
}

function getMesesSeverity(meses) {
  if (meses > 3) return 'danger';
  if (meses > 2) return 'warning';
  if (meses > 1) return 'info';
  return 'success';
}

function getAcaoSeverity(acao) {
  switch (acao) {
    case 'MANTER': return 'success';
    case 'TROCAR_USINA': return 'warning';
    case 'EXCLUIDO': return 'danger';
    default: return 'info';
  }
}

function formatarAcao(acao) {
  switch (acao) {
    case 'MANTER': return 'Manter';
    case 'TROCAR_USINA': return 'Trocar Usina';
    case 'EXCLUIDO': return 'Excluído';
    default: return acao;
  }
}

function getBadgeSeverity() {
  if (!resultadoRateio.value) return 'info';
  
  switch (resultadoRateio.value.status) {
    case 'RASCUNHO': return 'warning';
    case 'FINALIZADO': return 'success';
    case 'APLICADO': return 'info';
    default: return 'info';
  }
}

function getStatusLabel() {
  if (!resultadoRateio.value) return '';
  
  switch (resultadoRateio.value.status) {
    case 'RASCUNHO': return 'Rascunho';
    case 'FINALIZADO': return 'Finalizado';
    case 'APLICADO': return 'Aplicado';
    default: return '';
  }
}

function atualizarTotalRateio() {
  // Computed property já recalcula automaticamente
}

function autoAjustarRateio() {
  if (!resultadoRateio.value || !resultadoRateio.value.detalhes || 
      resultadoRateio.value.status !== 'RASCUNHO') return;
  
  const detalhes = resultadoRateio.value.detalhes;
  const total = totalRateio.value;
  
  if (total === 100) return; // Já está correto
  
  // Filtrar UCs que não estão com estoque suficiente e ordenar por consumo
  const ucsAjustaveis = detalhes
    .filter(d => !d.estoque_suficiente && d.acao !== 'EXCLUIDO')
    .sort((a, b) => b.unidade_consumidora.consumo_medio - a.unidade_consumidora.consumo_medio);
  
  if (ucsAjustaveis.length === 0) {
    toast.add({
      severity: 'warn',
      summary: 'Atenção',
      detail: 'Não há UCs disponíveis para ajuste automático',
      life: 3000
    });
    return;
  }
  
  if (total > 100) {
    // Reduzir proporcionalmente
    const excesso = total - 100;
    const fatorReducao = excesso / total;
    
    for (const uc of ucsAjustaveis) {
      const reducao = uc.porcentagem * fatorReducao;
      uc.porcentagem = Math.max(0.01, parseFloat((uc.porcentagem - reducao).toFixed(2)));
    }
  } else {
    // Aumentar para a UC com maior consumo
    const deficit = 100 - total;
    ucsAjustaveis[0].porcentagem = parseFloat((ucsAjustaveis[0].porcentagem + deficit).toFixed(2));
  }
  
  toast.add({
    severity: 'success',
    summary: 'Ajuste Concluído',
    detail: 'Rateio ajustado automaticamente para 100%',
    life: 3000
  });
}

async function finalizarRateio() {
  if (!resultadoRateio.value || totalRateio.value !== 100) return;
  
  confirm.require({
    message: 'Deseja realmente finalizar este rateio? Esta ação não poderá ser desfeita.',
    header: 'Confirmar Finalização',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Sim, finalizar',
    rejectLabel: 'Cancelar',
    accept: async () => {
      loading.value.finalizacao = true;
      
      try {
        // Demo: Simular chamada de API
        await new Promise(resolve => setTimeout(resolve, 800));
        
        // Atualizar status
        resultadoRateio.value.status = 'FINALIZADO';
        resultadoRateio.value.data_finalizacao = new Date().toISOString();
        
        toast.add({
          severity: 'success',
          summary: 'Rateio Finalizado',
          detail: 'O rateio foi finalizado com sucesso e está pronto para ser aplicado',
          life: 3000
        });
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Erro',
          detail: 'Falha ao finalizar o rateio',
          life: 3000
        });
      } finally {
        loading.value.finalizacao = false;
      }
    }
  });
}

async function exportarExcel() {
  if (!resultadoRateio.value || !resultadoRateio.value.id) return;
  
  try {
    loading.value.tabela = true;
    
    // Demo: Simular download
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    toast.add({
      severity: 'success',
      summary: 'Excel Gerado',
      detail: 'O arquivo foi gerado com sucesso',
      life: 3000
    });
    
    // Em uma aplicação real, isto faria download do arquivo
    // Aqui simulamos uma mensagem apenas
    toast.add({
      severity: 'info',
      summary: 'Demo de Download',
      detail: `Arquivo: rateio_${resultadoRateio.value.id}_${selectedUsina.value.nome}.xlsx`,
      life: 5000
    });
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Erro',
      detail: 'Falha ao exportar Excel',
      life: 3000
    });
  } finally {
    loading.value.tabela = false;
  }
}

function verUCs(usinaId) {
  router.push({
    name: 'ucs',
    query: { usina: usinaId }
  });
}

// Lifecycle hooks
onMounted(async () => {
  await carregarUsinas();
});
</script>
<style scoped>
.rateio-container {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

/* Hack para tornar as tabelas mais legíveis */
:deep(.p-datatable .p-datatable-tbody > tr) {
  box-shadow: none !important;
}

:deep(.p-datatable .p-datatable-tbody > tr:nth-child(even)) {
  background-color: #f9fafb;
}
</style>