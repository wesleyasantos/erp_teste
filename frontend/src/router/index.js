import { createRouter, createWebHistory } from 'vue-router';

// Importação das views
import DashboardView from '@/views/dashboard/DashboardView.vue';

// Módulo de Rateio
import RateioView from '@/views/rateio/RateioView.vue';
import UsinasView from '@/views/rateio/UsinasView.vue';
import UCsView from '@/views/rateio/UCsView.vue';
import HistoricoRateioView from '@/views/rateio/HistoricoRateioView.vue';

// Outros módulos do ERP
import FinanceView from '@/views/finance/FinanceView.vue';
import InventoryView from '@/views/inventory/InventoryView.vue';
import SalesView from '@/views/sales/SalesView.vue';
import PurchasesView from '@/views/purchases/PurchasesView.vue';
import HRView from '@/views/hr/HRView.vue';
import CRMView from '@/views/crm/CRMView.vue';
import ReportsView from '@/views/reports/ReportsView.vue';

// Autenticação
import LoginView from '@/views/auth/LoginView.vue';
import ProfileView from '@/views/auth/ProfileView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    
    // Módulo de Rateio
    {
      path: '/rateio',
      name: 'rateio',
      component: RateioView,
      meta: { requiresAuth: true }
    },
    {
      path: '/usinas',
      name: 'usinas',
      component: UsinasView,
      meta: { requiresAuth: true }
    },
    {
      path: '/unidades-consumidoras',
      name: 'ucs',
      component: UCsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/historico-rateio',
      name: 'historico-rateio',
      component: HistoricoRateioView,
      meta: { requiresAuth: true }
    },
    
    // Outros módulos
    {
      path: '/financeiro',
      name: 'finance',
      component: FinanceView,
      meta: { requiresAuth: true }
    },
    {
      path: '/estoque',
      name: 'inventory',
      component: InventoryView,
      meta: { requiresAuth: true }
    },
    {
      path: '/vendas',
      name: 'sales',
      component: SalesView,
      meta: { requiresAuth: true }
    },
    {
      path: '/compras',
      name: 'purchases',
      component: PurchasesView,
      meta: { requiresAuth: true }
    },
    {
      path: '/rh',
      name: 'hr',
      component: HRView,
      meta: { requiresAuth: true }
    },
    {
      path: '/crm',
      name: 'crm',
      component: CRMView,
      meta: { requiresAuth: true }
    },
    {
      path: '/relatorios',
      name: 'reports',
      component: ReportsView,
      meta: { requiresAuth: true }
    },
    
    // Autenticação
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guest: true }
    },
    {
      path: '/perfil',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }
    }
  ]
});

// Proteção de rotas
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('token');
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isLoggedIn) {
      next({ name: 'login', query: { redirect: to.fullPath } });
    } else {
      next();
    }
  } else if (to.matched.some(record => record.meta.guest)) {
    if (isLoggedIn) {
      next({ name: 'dashboard' });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;