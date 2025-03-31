import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

// PrimeVue e componentes
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import Tooltip from 'primevue/tooltip';

// PrimeVue componentes
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Dropdown from 'primevue/dropdown';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Menu from 'primevue/menu';
import Chart from 'primevue/chart';
import Dialog from 'primevue/dialog';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';
import Tag from 'primevue/tag';
import Avatar from 'primevue/avatar';
import Checkbox from 'primevue/checkbox';
// import TriStateCheckbox from 'primevue/tristatecheckbox';
import ProgressBar from 'primevue/progressbar';
import Message from 'primevue/message';

// Estilos
// import 'primevue/resources/themes/lara-light-indigo/theme.css';    // tema
// import 'primevue/resources/primevue.min.css';                      // core
// import 'primeicons/primeicons.css';                                // ícones
import 'primeflex/primeflex.css';
import './assets/styles/global.css';

// Demo Interceptors para simulação de backend
import { setupDemoInterceptors } from './views/demo/apiInterceptors';
setupDemoInterceptors();

const app = createApp(App);

// Pinia para gerenciamento de estado
const pinia = createPinia();
app.use(pinia);

// Router
app.use(router);

// PrimeVue
app.use(PrimeVue, { ripple: true });
app.use(ConfirmationService);
app.use(ToastService);
app.directive('tooltip', Tooltip);

// Registrar componentes globalmente
app.component('Button', Button);
app.component('InputText', InputText);
app.component('InputNumber', InputNumber);
app.component('Dropdown', Dropdown);
app.component('DataTable', DataTable);
app.component('Column', Column);
app.component('Menu', Menu);
app.component('Chart', Chart);
app.component('Dialog', Dialog);
app.component('Toast', Toast);
app.component('ConfirmDialog', ConfirmDialog);
app.component('Tag', Tag);
app.component('Avatar', Avatar);
app.component('Checkbox', Checkbox);
// app.component('TriStateCheckbox', TriStateCheckbox);
app.component('ProgressBar', ProgressBar);
app.component('Message', Message);

app.mount('#app');