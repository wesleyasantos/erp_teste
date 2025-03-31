<!-- src/views/dashboard/DashboardView.vue -->
<template>
    <div class="dashboard-container">
      <div class="grid">
        <!-- Status Cards -->
        <div class="col-12 md:col-6 xl:col-3">
          <div class="card mb-0">
            <div class="flex justify-content-between mb-3">
              <div>
                <span class="block text-500 font-medium mb-3">Usinas Ativas</span>
                <div class="text-900 font-medium text-xl">{{ numeroUsinas }}</div>
              </div>
              <div class="flex align-items-center justify-content-center bg-blue-100 border-round" style="width:2.5rem;height:2.5rem">
                <i class="pi pi-bolt text-blue-500 text-xl"></i>
              </div>
            </div>
            <span class="text-green-500 font-medium">{{ usinasAtivas }}% ativas </span>
            <span class="text-500">desde o último mês</span>
          </div>
        </div>
        
        <div class="col-12 md:col-6 xl:col-3">
          <div class="card mb-0">
            <div class="flex justify-content-between mb-3">
              <div>
                <span class="block text-500 font-medium mb-3">Unidades Consumidoras</span>
                <div class="text-900 font-medium text-xl">{{ numeroUCs }}</div>
              </div>
              <div class="flex align-items-center justify-content-center bg-orange-100 border-round" style="width:2.5rem;height:2.5rem">
                <i class="pi pi-th-large text-orange-500 text-xl"></i>
              </div>
            </div>
            <span class="text-green-500 font-medium">+{{ novasUCs }} </span>
            <span class="text-500">no último mês</span>
          </div>
        </div>
        
        <div class="col-12 md:col-6 xl:col-3">
          <div class="card mb-0">
            <div class="flex justify-content-between mb-3">
              <div>
                <span class="block text-500 font-medium mb-3">kWh Gerados (Mês)</span>
                <div class="text-900 font-medium text-xl">{{ formatNumber(kwhGerados) }}</div>
              </div>
              <div class="flex align-items-center justify-content-center bg-cyan-100 border-round" style="width:2.5rem;height:2.5rem">
                <i class="pi pi-sun text-cyan-500 text-xl"></i>
              </div>
            </div>
            <span class="text-green-500 font-medium">{{ aumentoKwh }}% </span>
            <span class="text-500">em relação ao mês anterior</span>
          </div>
        </div>
        
        <div class="col-12 md:col-6 xl:col-3">
          <div class="card mb-0">
            <div class="flex justify-content-between mb-3">
              <div>
                <span class="block text-500 font-medium mb-3">Rateios Pendentes</span>
          <div class="text-900 font-medium text-xl">{{ rateiosPendentes }}</div>
        </div>
        <div class="flex align-items-center justify-content-center bg-purple-100 border-round" style="width:2.5rem;height:2.5rem">
          <i class="pi pi-clock text-purple-500 text-xl"></i>
        </div>
      </div>
      <span class="text-500">Próximo rateio em </span>
      <span class="text-blue-500 font-medium">{{ diasProximoRateio }} dias</span>
    </div>
  </div>
  
  <!-- Gráfico de Geração/Consumo -->
  <div class="col-12 xl:col-8">
    <div class="card">
      <h5>Geração vs. Consumo (últimos 6 meses)</h5>
      <Chart type="line" :data="chartData" :options="chartOptions" class="h-20rem" />
    </div>
  </div>
  
  <!-- Próximos Rateios -->
  <div class="col-12 xl:col-4">
    <div class="card">
      <div class="flex justify-content-between align-items-center mb-4">
        <h5 class="m-0">Próximos Rateios</h5>
        <Button 
          label="Novo Rateio" 
          icon="pi pi-plus" 
          size="small"
          @click="$router.push('/rateio')"
        />
      </div>
      
      <ul class="list-none p-0 m-0">
        <li v-for="(rateio, index) in proximosRateios" :key="index" 
            class="flex align-items-center py-2 border-bottom-1 surface-border"
            :class="{'border-none': index === proximosRateios.length - 1}">
          <div class="flex-shrink-0 border-round mr-3 p-2"
              :class="getBgColorByDays(rateio.dias)">
            <i class="pi pi-calendar text-xl"></i>
          </div>
          <div class="flex-1">
            <span class="text-900 font-medium block mb-1">{{ rateio.usina }}</span>
            <div class="flex align-items-center">
              <i class="pi pi-clock text-500 mr-1"></i>
              <span class="text-500">{{ rateio.data }}</span>
            </div>
          </div>
          <Button 
            icon="pi pi-arrow-right" 
            text 
            rounded 
            @click="iniciarRateio(rateio.id)"
          />
        </li>
      </ul>
      
      <div class="flex justify-content-center mt-4">
        <Button 
          label="Ver Todos" 
          icon="pi pi-list" 
          text
          @click="$router.push('/historico-rateio')"
        />
      </div>
    </div>
  </div>
  
  <!-- Usinas com Maior Geração -->
  <div class="col-12 md:col-6">
    <div class="card">
      <div class="flex justify-content-between align-items-center mb-4">
        <h5 class="m-0">Usinas com Maior Geração</h5>
        <Button 
          icon="pi pi-external-link" 
          text 
          rounded
          @click="$router.push('/usinas')"
        />
      </div>
      
      <DataTable :value="usinasTop" class="p-datatable-sm" stripedRows>
        <Column field="nome" header="Usina"></Column>
        <Column field="grupo" header="Grupo">
          <template #body="slotProps">
            <Tag 
              :severity="slotProps.data.grupo === 'A' ? 'info' : 'success'" 
              :value="'Grupo ' + slotProps.data.grupo"
            />
          </template>
        </Column>
        <Column field="geracao" header="Geração (kWh)">
          <template #body="slotProps">
            {{ formatNumber(slotProps.data.geracao) }}
          </template>
        </Column>
        <Column field="percentual" header="% do Total">
          <template #body="slotProps">
            <div class="flex align-items-center">
              <div class="w-7rem mr-2">
                <ProgressBar :value="slotProps.data.percentual" :showValue="false" :style="{ height: '6px' }" />
              </div>
              <span>{{ slotProps.data.percentual }}%</span>
            </div>
          </template>
        </Column>
        <Column>
          <template #body="slotProps">
            <Button 
              icon="pi pi-share-alt" 
              text 
              rounded
              @click="iniciarRateio(slotProps.data.id)"
              tooltip="Iniciar rateio"
              tooltipOptions="top"
            />
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
  
  <!-- UCs com Estoque Crítico -->
  <div class="col-12 md:col-6">
    <div class="card">
      <div class="flex justify-content-between align-items-center mb-4">
        <h5 class="m-0">UCs com Estoque Crítico</h5>
        <Button 
          icon="pi pi-external-link" 
          text 
          rounded
          @click="$router.push('/unidades-consumidoras')"
        />
      </div>
      
      <DataTable :value="ucsEstoqueCritico" class="p-datatable-sm" stripedRows>
        <Column field="codigo" header="Código"></Column>
        <Column field="nome" header="Nome"></Column>
        <Column field="estoque" header="Estoque (kWh)">
          <template #body="slotProps">
            {{ formatNumber(slotProps.data.estoque) }}
          </template>
        </Column>
        <Column field="consumo" header="Consumo Médio">
          <template #body="slotProps">
            {{ formatNumber(slotProps.data.consumo) }}
          </template>
        </Column>
        <Column field="meses" header="Meses Estoque">
          <template #body="slotProps">
            <Tag :severity="getMesesSeverity(slotProps.data.meses)">
              {{ slotProps.data.meses.toFixed(1) }}
            </Tag>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</div>
  </div>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import Chart from 'primevue/chart';

const router = useRouter();

// Estado
const numeroUsinas = ref(12);
const usinasAtivas = ref(92);
const numeroUCs = ref(87);
const novasUCs = ref(14);
const kwhGerados = ref(238500);
const aumentoKwh = ref(12.5);
const rateiosPendentes = ref(5);
const diasProximoRateio = ref(3);

const proximosRateios = ref([
  { id: 1, usina: 'Usina Solar Horizonte', data: '05/04/2025', dias: 3 },
  { id: 2, usina: 'Usina Eólica Norte', data: '10/04/2025', dias: 8 },
  { id: 3, usina: 'Usina Solar Meridional', data: '16/04/2025', dias: 14 },
  { id: 4, usina: 'Usina Fotovoltaica Central', data: '22/04/2025', dias: 20 }
]);

const usinasTop = ref([
  { id: 1, nome: 'Usina Solar Horizonte', grupo: 'A', geracao: 58420, percentual: 24.5 },
  { id: 3, nome: 'Usina Solar Meridional', grupo: 'A', geracao: 45800, percentual: 19.2 },
  { id: 2, nome: 'Usina Eólica Norte', grupo: 'B', geracao: 35200, percentual: 14.8 },
  { id: 4, nome: 'Usina Fotovoltaica Central', grupo: 'B', geracao: 22500, percentual: 9.4 }
]);

const ucsEstoqueCritico = ref([
  { id: 1, codigo: 'UC100342', nome: 'Supermercado Sul', estoque: 180, consumo: 520, meses: 0.35 },
  { id: 2, codigo: 'UC105689', nome: 'Shopping Plaza', estoque: 350, consumo: 850, meses: 0.41 },
  { id: 3, codigo: 'UC104521', nome: 'Indústria Têxtil', estoque: 620, consumo: 1250, meses: 0.50 },
  { id: 4, codigo: 'UC102387', nome: 'Hospital Central', estoque: 780, consumo: 1450, meses: 0.54 },
  { id: 5, codigo: 'UC107654', nome: 'Faculdade Norte', estoque: 450, consumo: 720, meses: 0.63 }
]);

// Dados do gráfico
const chartData = ref({
  labels: ['Outubro', 'Novembro', 'Dezembro', 'Janeiro', 'Fevereiro', 'Março'],
  datasets: [
    {
      label: 'Geração Total (kWh)',
      data: [180000, 195000, 205000, 215000, 228000, 238500],
      borderColor: '#4F46E5',
      backgroundColor: 'rgba(79, 70, 229, 0.1)',
      fill: true,
      tension: 0.4
    },
    {
      label: 'Consumo Total (kWh)',
      data: [170000, 182000, 190000, 198000, 210000, 225000],
      borderColor: '#10B981',
      backgroundColor: 'rgba(16, 185, 129, 0.1)',
      fill: true,
      tension: 0.4
    }
  ]
});

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      align: 'end'
    },
    tooltip: {
      mode: 'index',
      intersect: false
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      }
    },
    y: {
      grid: {
        display: true,
        drawBorder: false
      },
      ticks: {
        callback: function(value) {
          return formatNumber(value);
        }
      }
    }
  }
});

// Methods
function formatNumber(value) {
  if (!value && value !== 0) return '';
  return new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 0 }).format(value);
}

function getBgColorByDays(dias) {
  if (dias <= 5) return 'bg-red-100 text-red-500';
  if (dias <= 10) return 'bg-orange-100 text-orange-500';
  return 'bg-blue-100 text-blue-500';
}

function getMesesSeverity(meses) {
  if (meses < 0.5) return 'danger';
  if (meses < 1) return 'warning';
  return 'success';
}

function iniciarRateio(usinaId) {
  router.push({
    path: '/rateio',
    query: { usina: usinaId }
  });
}

// Lifecycle hooks
onMounted(() => {
  // Em uma aplicação real, aqui você carregaria os dados da API
});
</script>
<style scoped>
.dashboard-container {
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
  height: 100%;
}

h5 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1E293B;
}
</style>