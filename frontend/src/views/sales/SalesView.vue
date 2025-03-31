<template>
    <div class="finance-container">
      <!-- Header Card -->
      <div class="card mb-3">
        <div class="flex flex-column md:flex-row md:align-items-center md:justify-content-between">
          <div class="mb-3 md:mb-0">
            <h2 class="mb-1 text-xl font-medium">Módulo Financeiro</h2>
            <p class="text-600 m-0">Demonstração do módulo financeiro</p>
          </div>
        </div>
      </div>
      
      <!-- Demo Content -->
      <div class="card">
        <div class="flex justify-content-center align-items-center p-5">
          <div class="text-center">
            <i class="pi pi-money-bill text-primary text-5xl mb-3"></i>
            <h3>Módulo em Demonstração</h3>
            <p class="text-600">
              Esta é uma tela de demonstração do módulo financeiro.<br>
              Módulo completo disponível na versão comercial.
            </p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  // Componente vazio para demonstração
  </script>
  
  <style scoped>
  .finance-container {
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