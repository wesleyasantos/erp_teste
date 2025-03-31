<template>
    <div class="ucs-container">
      <!-- Header Card -->
      <div class="card mb-3">
        <div class="flex flex-column md:flex-row md:align-items-center md:justify-content-between">
          <div class="mb-3 md:mb-0">
            <h2 class="mb-1 text-xl font-medium">Unidades Consumidoras</h2>
            <p class="text-600 m-0">Gerencie as unidades consumidoras vinculadas às usinas</p>
          </div>
          <Button 
            label="Nova UC" 
            icon="pi pi-plus" 
            @click="abrirDialogUC()"
          />
        </div>
      </div>
      
      <!-- Conteúdo principal -->
      <div class="card">
        <p>Conteúdo da página de Unidades Consumidoras será implementado aqui.</p>
        <p>Página em construção.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  // Estado
  const dialogVisible = ref(false);
  
  // Methods
  function abrirDialogUC() {
    dialogVisible.value = true;
  }
  </script>
  
  <style scoped>
  .ucs-container {
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
  </style>