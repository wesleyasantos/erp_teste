## 5. Tela de Gestão de Usinas

```vue
<!-- src/views/rateio/UsinasView.vue -->
<template>
  <div class="usinas-container">
    <!-- Header Card -->
    <div class="card mb-3">
      <div class="flex flex-column md:flex-row md:align-items-center md:justify-content-between">
        <div class="mb-3 md:mb-0">
          <h2 class="mb-1 text-xl font-medium">Gestão de Usinas</h2>
          <p class="text-600 m-0">Cadastre e gerencie as usinas para rateio de energia</p>
        </div>
        <Button 
          label="Nova Usina" 
          icon="pi pi-plus" 
          @click="abrirDialogUsina()"
        />
      </div>
    </div>
    
    <!-- Tabela de Usinas -->
    <div class="card">
      <DataTable 
        :value="usinas" 
        :paginator="true" 
        :rows="10"
        :rowsPerPageOptions="[5, 10, 25, 50]"
        responsiveLayout="scroll"
        stripedRows
        v-model:filters="filters"
        filterDisplay="menu"
        :loading="loading"
        :globalFilterFields="['nome', 'grupo']"
      >
        <template #header>
          <div class="flex justify-content-between">
            <Button 
              icon="pi pi-refresh" 
              text 
              @click="carregarUsinas"
              :loading="loading"
            />
            <span class="p-input-icon-left">
              <i class="pi pi-search" />
              <InputText v-model="filters['global'].value" placeholder="Buscar..." />
            </span>
          </div>
        </template>
        
        <Column field="nome" header="Nome" :sortable="true" style="min-width: 12rem">
          <template #body="slotProps">
            <div class="flex align-items-center">
              <Avatar :icon="getGrupoIcon(slotProps.data.grupo)" 
                      :style="getGrupoAvatarStyle(slotProps.data.grupo)" 
                      shape="circle" />
              <div class="ml-2">
                <span class="font-bold">{{ slotProps.data.nome }}</span>
                <div class="text-xs text-500">Cadastrada em {{ formatDate(slotProps.data.data_cadastro) }}</div>
              </div>
            </div>
          </template>
        </Column>
        
        <Column field="grupo" header="Grupo" :sortable="true" style="min-width: 8rem">
          <template #body="slotProps">
            <Tag 
              :severity="slotProps.data.grupo === 'A' ? 'info' : 'success'" 
              :value="'Grupo ' + slotProps.data.grupo"
            />
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <Dropdown 
              v-model="filterModel.value" 
              @change="filterCallback()"
              :options="gruposOptions" 
              optionLabel="label" 
              optionValue="value"
              placeholder="Selecionar grupo" 
              class="p-column-filter"
              showClear
            />
          </template>
        </Column>
        
        <Column field="media_transferencia" header="Média (kWh)" :sortable="true" style="min-width: 10rem">
          <template #body="slotProps">
            {{ formatNumber(slotProps.data.media_transferencia) }}
          </template>
        </Column>
        
        <Column field="dia_faturamento" header="Dia Faturamento" :sortable="true" style="min-width: 10rem">
          <template #body="slotProps">
            <div class="flex align-items-center">
              <i class="pi pi-calendar text-primary-500 mr-2"></i>
              <span>Dia {{ slotProps.data.dia_faturamento }}</span>
            </div>
          </template>
        </Column>
        
        <Column field="total_ucs" header="UCs Vinculadas" :sortable="true" style="min-width: 10rem">
          <template #body="slotProps">
            <div class="flex align-items-center">
              <i class="pi pi-users text-blue-500 mr-2"></i>
              <span>{{ slotProps.data.total_ucs }}</span>
            </div>
          </template>
        </Column>
        
        <Column field="ativa" header="Status" :sortable="true" style="min-width: 8rem">
          <template #body="slotProps">
            <Tag 
              :severity="slotProps.data.ativa ? 'success' : 'danger'" 
              :value="slotProps.data.ativa ? 'Ativa' : 'Inativa'"
            />
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <TriStateCheckbox v-model="filterModel.value" @change="filterCallback()" />
          </template>
        </Column>
        
        <Column header="Ações" style="min-width: 10rem">
          <template #body="slotProps">
            <div class="flex gap-2">
              <Button 
                icon="pi pi-calculator" 
                text 
                rounded 
                severity="info" 
                v-tooltip.top="'Criar rateio'"
                @click="criarRateio(slotProps.data.id)"
              />
              <Button 
                icon="pi pi-users" 
                text 
                rounded 
                severity="secondary" 
                v-tooltip.top="'Ver UCs vinculadas'"
                @click="verUCsVinculadas(slotProps.data.id)"
              />
              <Button 
                icon="pi pi-pencil" 
                text 
                rounded 
                v-tooltip.top="'Editar'"
                @click="abrirDialogUsina(slotProps.data)"
              />
              <Button 
                icon="pi pi-trash" 
                text 
                rounded 
                severity="danger" 
                v-tooltip.top="'Excluir'"
                @click="confirmarExclusao(slotProps.data)"
              />
            </div>
          </template>
        </Column>
        
        <template #empty>
          <div class="p-4 text-center">
            <i class="pi pi-info-circle text-blue-500 text-3xl mb-3 block"></i>
            <span>Nenhuma usina encontrada.</span>
          </div>
        </template>
      </DataTable>
    </div>
    
    <!-- Dialog para adicionar/editar usina -->
    <Dialog 
      v-model:visible="dialogVisible" 
      :style="{width: '550px'}" 
      header="Cadastro de Usina" 
      :modal="true"
      :closable="!salvando"
      :closeOnEscape="!salvando"
    >
      <div class="p-fluid">
        <div class="field mb-4">
          <label for="nome" class="font-medium mb-2 block">Nome da Usina <span class="text-danger">*</span></label>
          <InputText 
            id="nome" 
            v-model.trim="usina.nome" 
            :class="{'p-invalid': submitted && !usina.nome}"
            placeholder="Ex: Usina Solar Central"
            required 
          />
          <small v-if="submitted && !usina.nome" class="p-error">Nome é obrigatório.</small>
        </div>
        
        <div class="grid">
          <div class="col-12 md:col-6 field mb-4">
            <label for="grupo" class="font-medium mb-2 block">Grupo <span class="text-danger">*</span></label>
            <Dropdown 
              id="grupo" 
              v-model="usina.grupo" 
              :options="[{label: 'Grupo A', value: 'A'}, {label: 'Grupo B', value: 'B'}]" 
              optionLabel="label" 
              optionValue="value"
              placeholder="Selecione o grupo"
              :class="{'p-invalid': submitted && !usina.grupo}"
            />
            <small v-if="submitted && !usina.grupo" class="p-error">Grupo é obrigatório.</small>
            <small class="text-600 block mt-1">
              Grupo A: Alta tensão | Grupo B: Baixa tensão
            </small>
          </div>
          
          <div class="col-12 md:col-6 field mb-4">
            <label for="dia" class="font-medium mb-2 block">Dia de Faturamento <span class="text-danger">*</span></label>
            <InputNumber 
              id="dia" 
              v-model="usina.dia_faturamento" 
              :min="1" 
              :max="31" 
              mode="decimal" 
              useGrouping="false"
              placeholder="1-31"
              :class="{'p-invalid': submitted && !usina.dia_faturamento}"
            />
            <small v-if="submitted && !usina.dia_faturamento" class="p-error">Dia é obrigatório.</small>
          </div>
        </div>
        
        <div class="field mb-4">
          <label for="media" class="font-medium mb-2 block">Média de Transferência (kWh) <span class="text-danger">*</span></label>
          <InputNumber 
            id="media" 
            v-model="usina.media_transferencia" 
            mode="decimal"
            :minFractionDigits="2" 
            :maxFractionDigits="2"
            placeholder="Ex: 10000.00"
            :class="{'p-invalid': submitted && !usina.media_transferencia}"
          />
          <small v-if="submitted && !usina.media_transferencia" class="p-error">Média é obrigatória.</small>
        </div>
        
        <div class="field mb-4">
          <div class="flex align-items-center">
            <Checkbox id="ativa" v-model="usina.ativa" :binary="true" />
            <label for="ativa" class="ml-2">Usina ativa para rateio</label>
          </div>
        </div>
      </div>
      
      <template #footer>
        <Button 
          label="Cancelar" 
          icon="pi pi-times" 
          text 
          @click="dialogVisible = false"
          :disabled="salvando"
        />
        <Button 
          label="Salvar" 
          icon="pi pi-check" 
          @click="salvarUsina"
          :loading="salvando"
        />
      </template>
    </Dialog>
    
    <!-- Dialog de confirmação de exclusão -->
    <ConfirmDialog></ConfirmDialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useConfirm } from 'primevue/useconfirm';
import { useToast } from 'primevue/usetoast';

const router = useRouter();
const confirm = useConfirm();
const toast = useToast();

// Estado
const usinas = ref([]);
const loading = ref(false);
const dialogVisible = ref(false);
const submitted = ref(false);
const salvando = ref(false);
const usina = ref({
  nome: '',
  grupo: null,
  media_transferencia: null,
  dia_faturamento: null,
  ativa: true
});

// Filtros
const filters = ref({
  'global': { value: null, matchMode: 'contains' },
  'grupo': { value: null, matchMode: 'equals' },
  'ativa': { value: null, matchMode: 'equals' }
});

const gruposOptions = [
  { label: 'Grupo A', value: 'A' },
  { label: 'Grupo B', value: 'B' }
];

// Methods
function formatNumber(value) {
  if (!value && value !== 0) return '';
  return new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 2 }).format(value);
}

function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('pt-BR', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric' 
  }).format(date);
}

function getGrupoIcon(grupo) {
  return grupo === 'A' ? 'pi pi-bolt' : 'pi pi-sun';
}

function getGrupoAvatarStyle(grupo) {
  return {
    backgroundColor: grupo === 'A' ? '#4F46E5' : '#10B981',
    color: '#FFFFFF'
  };
}

async function carregarUsinas() {
  loading.value = true;
  
  try {
    // Demo: Simular chamada de API
    await new Promise(resolve => setTimeout(resolve, 800));
    
    usinas.value = [
      { 
        id: 1, 
        nome: 'Usina Solar Horizonte', 
        grupo: 'A', 
        media_transferencia: 15000, 
        dia_faturamento: 10, 
        total_ucs: 8,
        ativa: true,
        data_cadastro: '2024-10-15T14:30:00Z'
      },
      { 
        id: 2, 
        nome: 'Usina Eólica Norte', 
        grupo: 'B', 
        media_transferencia: 8500, 
        dia_faturamento: 15, 
        total_ucs: 12,
        ativa: true,
        data_cadastro: '2024-09-22T10:15:00Z'
      },
      { 
        id: 3, 
        nome: 'Usina Solar Meridional', 
        grupo: 'A', 
        media_transferencia: 22000, 
        dia_faturamento: 5, 
        total_ucs: 15,
        ativa: true,
        data_cadastro: '2024-11-08T09:45:00Z'
      },
      { 
        id: 4, 
        nome: 'Usina Fotovoltaica Central', 
        grupo: 'B', 
        media_transferencia: 7200, 
        dia_faturamento: 20, 
        total_ucs: 6,
        ativa: true,
        data_cadastro: '2025-01-17T16:20:00Z'
      },
      { 
        id: 5, 
        nome: 'Usina Solar Vale Verde', 
        grupo: 'A', 
        media_transferencia: 18500, 
        dia_faturamento: 25, 
        total_ucs: 10,
        ativa: false,
        data_cadastro: '2025-02-03T11:10:00Z'
      }
    ];
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Erro',
      detail: 'Falha ao carregar usinas',
      life: 3000
    });
  } finally {
    loading.value = false;
  }
}

function abrirDialogUsina(usinaData = null) {
  submitted.value = false;
  
  if (usinaData) {
    // Editar - clone para não modificar diretamente
    usina.value = { ...usinaData };
  } else {
    // Nova usina
    usina.value = {
      nome: '',
      grupo: null,
      media_transferencia: null,
      dia_faturamento: null,
      ativa: true
    };
  }
  
  dialogVisible.value = true;
}

async function salvarUsina() {
  submitted.value = true;
  
  // Validação
  if (!usina.value.nome || !usina.value.grupo || 
      !usina.value.media_transferencia || !usina.value.dia_faturamento) {
    toast.add({
      severity: 'warn',
      summary: 'Atenção',
      detail: 'Preencha todos os campos obrigatórios',
      life: 3000
    });
    return;
  }
  
  salvando.value = true;
  
  try {
    // Demo: Simular chamada de API
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    if (usina.value.id) {
      // Atualizar existente
      const index = usinas.value.findIndex(u => u.id === usina.value.id);
      if (index !== -1) {
        usinas.value[index] = { ...usina.value };
      }
      
      toast.add({
        severity: 'success',
        summary: 'Sucesso',
        detail: 'Usina atualizada com sucesso',
        life: 3000
      });
    } else {
      // Criar nova
      const novaUsina = { 
        ...usina.value, 
        id: Math.floor(Math.random() * 1000) + 10,
        data_cadastro: new Date().toISOString(),
        total_ucs: 0
      };
      
      usinas.value.unshift(novaUsina);
      
      toast.add({
        severity: 'success',
        summary: 'Sucesso',
       detail: 'Usina cadastrada com sucesso',
       life: 3000
     });
   }
   
   dialogVisible.value = false;
 } catch (error) {
   toast.add({
     severity: 'error',
     summary: 'Erro',
     detail: 'Falha ao salvar usina',
     life: 3000
   });
 } finally {
   salvando.value = false;
 }
}

function confirmarExclusao(usinaData) {
 confirm.require({
   message: `Deseja realmente excluir a usina "${usinaData.nome}"?`,
   header: 'Confirmar Exclusão',
   icon: 'pi pi-exclamation-triangle',
   acceptClass: 'p-button-danger',
   acceptLabel: 'Sim, excluir',
   rejectLabel: 'Cancelar',
   accept: () => excluirUsina(usinaData.id)
 });
}

async function excluirUsina(id) {
 loading.value = true;
 
 try {
   // Demo: Simular chamada de API
   await new Promise(resolve => setTimeout(resolve, 800));
   
   // Remover do array local
   usinas.value = usinas.value.filter(u => u.id !== id);
   
   toast.add({
     severity: 'success',
     summary: 'Sucesso',
     detail: 'Usina excluída com sucesso',
     life: 3000
   });
 } catch (error) {
   toast.add({
     severity: 'error',
     summary: 'Erro',
     detail: 'Falha ao excluir usina',
     life: 3000
   });
 } finally {
   loading.value = false;
 }
}

function criarRateio(usinaId) {
 router.push({
   path: '/rateio',
   query: { usina: usinaId }
 });
}

function verUCsVinculadas(usinaId) {
 router.push({
   path: '/unidades-consumidoras',
   query: { usina: usinaId }
 });
}

// Lifecycle hooks
onMounted(async () => {
 await carregarUsinas();
});
</script>

<style scoped>
.usinas-container {
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

:deep(.p-datatable .p-datatable-thead > tr > th) {
 background-color: #f8fafc;
}

:deep(.p-dialog-content) {
 padding-top: 2rem;
}

.text-danger {
 color: #ef4444;
}
</style>