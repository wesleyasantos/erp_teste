<template>
  <div class="layout-wrapper" :class="{'sidebar-collapsed': !sidebarExpanded}">
    <!-- Sidebar -->
    <aside class="sidebar" v-if="isLoggedIn">
      <div class="sidebar-header">
        <div class="logo-container">
          <img src="/logo.png" alt="Logo" class="logo-img" />
          <span v-if="sidebarExpanded" class="logo-text">ERP Complete</span>
        </div>
        <button class="sidebar-toggle" @click="toggleSidebar">
          <i class="pi" :class="sidebarExpanded ? 'pi-chevron-left' : 'pi-chevron-right'"></i>
        </button>
      </div>
      
      <div class="sidebar-content">
        <Menu :model="menuItems" class="sidebar-menu" />
      </div>
      
      <div class="sidebar-footer" v-if="sidebarExpanded">
        <div class="user-info">
          <Avatar icon="pi pi-user" class="mr-2" />
          <div class="user-details">
            <div class="user-name">Administrador</div>
            <div class="user-role">Demonstração</div>
          </div>
        </div>
        <Button 
          icon="pi pi-sign-out" 
          label="Sair" 
          text 
          class="w-full mt-2" 
          @click="logout" 
        />
      </div>
    </aside>
    
    <!-- Main Content -->
    <div class="main-content">
      <header class="topbar" v-if="isLoggedIn">
        <div class="topbar-left">
          <button class="menu-button" @click="toggleSidebar">
            <i class="pi pi-bars"></i>
          </button>
          <h1 class="page-title">{{ currentPageTitle }}</h1>
        </div>
        
        <div class="topbar-right">
          <span class="demo-badge">DEMO</span>
          <Button icon="pi pi-bell" text rounded class="mr-2" />
          <Button icon="pi pi-cog" text rounded class="mr-2" />
          <Menu ref="userMenu" :model="userMenuItems" :popup="true" />
          <Button 
            icon="pi pi-user" 
            text 
            rounded 
            aria-label="Menu de usuário"
            @click="toggleUserMenu"
          />
        </div>
      </header>
      
      <main class="content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
      
      <footer class="footer" v-if="isLoggedIn">
        <div>&copy; 2025 ERP Complete - Versão Demo</div>
      </footer>
    </div>
    
    <!-- Toast -->
    <Toast position="bottom-right" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const sidebarExpanded = ref(true);
const userMenu = ref(null);

// Computed properties
const isLoggedIn = computed(() => {
  return localStorage.getItem('auth_token') !== null;
});

const currentPageTitle = computed(() => {
  const titles = {
    'dashboard': 'Dashboard',
    'rateio': 'Rateio de Energia',
    'usinas': 'Gestão de Usinas',
    'ucs': 'Unidades Consumidoras',
    'historico-rateio': 'Histórico de Rateios',
    'finance': 'Financeiro',
    'inventory': 'Estoque',
    'sales': 'Vendas',
    'purchases': 'Compras',
    'hr': 'Recursos Humanos',
    'crm': 'CRM',
    'reports': 'Relatórios'
  };
  
  return titles[route.name] || 'Dashboard';
});

// Menu items
const menuItems = ref([
  {
    label: 'Principal',
    items: [
      {
        label: 'Dashboard',
        icon: 'pi pi-home',
        to: '/'
      }
    ]
  },
  {
    label: 'Rateio de Energia',
    items: [
      {
        label: 'Calcular Rateio',
        icon: 'pi pi-calculator',
        to: '/rateio'
      },
      {
        label: 'Usinas',
        icon: 'pi pi-bolt',
        to: '/usinas'
      },
      {
        label: 'Unidades Consumidoras',
        icon: 'pi pi-th-large',
        to: '/unidades-consumidoras'
      },
      {
        label: 'Histórico',
        icon: 'pi pi-history',
        to: '/historico-rateio'
      }
    ]
  },
  {
    label: 'Outros Módulos',
    items: [
      {
        label: 'Financeiro',
        icon: 'pi pi-money-bill',
        to: '/financeiro',
        class: 'demo-item'
      },
      {
        label: 'Estoque',
        icon: 'pi pi-box',
        to: '/estoque',
        class: 'demo-item'
      },
      {
        label: 'Vendas',
        icon: 'pi pi-shopping-cart',
        to: '/vendas',
        class: 'demo-item'
      },
      {
        label: 'Compras',
        icon: 'pi pi-shopping-bag',
        to: '/compras',
        class: 'demo-item'
      },
      {
        label: 'RH',
        icon: 'pi pi-users',
        to: '/rh',
        class: 'demo-item'
      },
      {
        label: 'CRM',
        icon: 'pi pi-star',
        to: '/crm',
        class: 'demo-item'
      },
      {
        label: 'Relatórios',
        icon: 'pi pi-chart-bar',
        to: '/relatorios',
        class: 'demo-item'
      }
    ]
  }
]);

// User menu items
const userMenuItems = ref([
  { label: 'Meu Perfil', icon: 'pi pi-user' },
  { label: 'Configurações', icon: 'pi pi-cog' },
  { separator: true },
  { label: 'Sair', icon: 'pi pi-power-off', command: logout }
]);

// Methods
function toggleSidebar() {
  sidebarExpanded.value = !sidebarExpanded.value;
}

function toggleUserMenu(event) {
  userMenu.value.toggle(event);
}

function logout() {
  localStorage.removeItem('auth_token');
  router.push('/login');
}

// Lifecycle hooks
onMounted(() => {
  // Set demo token if not present
  if (!localStorage.getItem('auth_token')) {
    localStorage.setItem('auth_token', 'demo_token');
  }
  
  // Handle responsive sidebar
  const handleResize = () => {
    if (window.innerWidth < 768) {
      sidebarExpanded.value = false;
    } else {
      sidebarExpanded.value = true;
    }
  };
  
  handleResize();
  window.addEventListener('resize', handleResize);
  
  return () => {
    window.removeEventListener('resize', handleResize);
  };
});
</script>

<style>
/* CSS Variables */
:root {
  --sidebar-width: 260px;
  --sidebar-width-collapsed: 70px;
  --sidebar-bg: #1E293B;
  --sidebar-text: #E2E8F0;
  --topbar-height: 64px;
  --topbar-bg: #FFFFFF;
  --footer-height: 50px;
  --primary-color: #4F46E5;
  --text-color: #1E293B;
  --text-muted: #64748B;
  --border-color: #E2E8F0;
  --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

/* Layout Structure */
.layout-wrapper {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: var(--sidebar-width);
  background-color: var(--sidebar-bg);
  color: var(--sidebar-text);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 1000;
  transition: width 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar-collapsed .sidebar {
  width: var(--sidebar-width-collapsed);
}

.main-content {
  flex: 1;
  margin-left: var(--sidebar-width);
  transition: margin-left 0.3s ease;
  display: flex;
  flex-direction: column;
}

.sidebar-collapsed .main-content {
  margin-left: var(--sidebar-width-collapsed);
}

/* Sidebar Components */
.sidebar-header {
  height: var(--topbar-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
  overflow: hidden;
}

.logo-img {
  width: 30px;
  height: 30px;
  object-fit: contain;
}

.logo-text {
  margin-left: 10px;
  font-size: 1.2rem;
  font-weight: 600;
  color: white;
  white-space: nowrap;
}

.sidebar-toggle {
  width: 28px;
  height: 28px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 4px;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.sidebar-toggle:hover {
  background: rgba(255, 255, 255, 0.2);
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 0;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
}

.user-details {
  overflow: hidden;
}

.user-name {
  font-weight: 600;
  color: white;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
}

/* Menu Customization */
:deep(.sidebar-menu) {
  background: transparent;
  border: none;
  width: 100%;
  padding: 0;
}

:deep(.sidebar-menu .p-menuitem-text),
:deep(.sidebar-menu .p-menuitem-icon) {
  color: var(--sidebar-text) !important;
}

:deep(.sidebar-menu .p-submenu-header) {
  background: transparent;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 1.25rem 1.25rem 0.5rem;
  border: none;
}

:deep(.sidebar-menu .p-menuitem) {
  margin: 0.25rem 0.75rem;
}

:deep(.sidebar-menu .p-menuitem-link) {
  padding: 0.75rem 1rem;
  border-radius: 6px;
  transition: all 0.3s;
}

:deep(.sidebar-menu .p-menuitem-link:hover) {
  background: rgba(255, 255, 255, 0.1);
}

:deep(.sidebar-menu .p-menuitem-link.router-link-active) {
  background: var(--primary-color) !important;
}

:deep(.sidebar-menu .p-menuitem-link.router-link-active .p-menuitem-text),
:deep(.sidebar-menu .p-menuitem-link.router-link-active .p-menuitem-icon) {
  color: white !important;
  font-weight: 500;
}

:deep(.sidebar-menu .demo-item .p-menuitem-text),
:deep(.sidebar-menu .demo-item .p-menuitem-icon) {
  opacity: 0.7;
}

/* When sidebar is collapsed */
.sidebar-collapsed :deep(.sidebar-menu .p-submenu-header) {
  display: none;
}

.sidebar-collapsed :deep(.sidebar-menu .p-menuitem-icon) {
  margin-right: 0;
}

.sidebar-collapsed :deep(.sidebar-menu .p-menuitem-text) {
  display: none;
}

.sidebar-collapsed :deep(.sidebar-menu .p-menuitem) {
  margin: 0.25rem;
  display: flex;
  justify-content: center;
}

.sidebar-collapsed :deep(.sidebar-menu .p-menuitem-link) {
  padding: 0.75rem;
  display: flex;
  justify-content: center;
}

/* Topbar */
.topbar {
  height: var(--topbar-height);
  background-color: var(--topbar-bg);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  position: sticky;
  top: 0;
  z-index: 999;
  box-shadow: var(--shadow);
}

.topbar-left {
  display: flex;
  align-items: center;
}

.menu-button {
  display: none;
  background: none;
  border: none;
  color: var(--text-color);
  font-size: 1.2rem;
  cursor: pointer;
  margin-right: 1rem;
}

.page-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.topbar-right {
  display: flex;
  align-items: center;
}

.demo-badge {
  background-color: #F59E0B;
  color: white;
  font-size: 0.7rem;
  font-weight: bold;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  margin-right: 1rem;
}

/* Content area */
.content {
  flex: 1;
  padding: 1.5rem;
  background-color: #F9FAFB;
}

/* Footer */
.footer {
  height: var(--footer-height);
  display: flex;
  align-items: center;
  justify-content: center;
  border-top: 1px solid var(--border-color);
  color: var(--text-muted);
  font-size: 0.875rem;
  background-color: white;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .sidebar {
    width: var(--sidebar-width);
    transform: translateX(-100%);
  }
  
  .sidebar-collapsed .sidebar {
    transform: translateX(0);
    width: var(--sidebar-width);
  }
  
  .main-content {
    margin-left: 0 !important;
  }
  
  .menu-button {
    display: block;
  }
  
  .sidebar-header {
    justify-content: space-between;
  }
}

@media (max-width: 576px) {
  .topbar {
    padding: 0 1rem;
  }
  
  .page-title {
    font-size: 1rem;
  }
  
  .content {
    padding: 1rem;
  }
  
  .demo-badge {
    display: none;
  }
}
</style>