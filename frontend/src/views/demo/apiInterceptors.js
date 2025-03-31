import axios from 'axios';

// Configuração inicial
axios.defaults.baseURL = 'https://api-demo.erpcomplete.com.br';

export function setupDemoInterceptors() {
  // Intercepta requisições para simular backend
  axios.interceptors.request.use(request => {
    console.log('Requisição interceptada:', request.url);
    
    // Simular delay para parecer real
    return new Promise(resolve => {
      setTimeout(() => {
        resolve(request);
      }, 300 + Math.random() * 500); // Delay entre 300-800ms
    });
  });
  
  // Intercepta respostas para simular backend
  axios.interceptors.response.use(
    response => {
      console.log('Resposta interceptada:', response.config.url);
      return response;
    },
    error => {
      console.log('Erro interceptado:', error.config?.url);
      
      // Converter erro para resposta de demonstração amigável
      // Isso garante que a demonstração não será interrompida por erros
      return Promise.resolve({
        data: {
          demo: true,
          error: true,
          message: 'Ocorreu um erro ao processar sua solicitação. Como este é um ambiente de demonstração, continuaremos com dados simulados.'
        }
      });
    }
  );
  
  // Adicionar token de demonstração para todas requisições
  axios.interceptors.request.use(config => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });
}