<template>
  <div class="login-page">
    <div class="login-container">
      <div class="logo-section">
        <img src="/logo.png" alt="ERP Complete Logo" class="logo-img" />
        <h1 class="app-name">ERP Complete</h1>
        <div class="app-version">Versão Demonstração</div>
      </div>
      
      <div class="login-card">
        <h2 class="card-title">Acesso ao Sistema</h2>
        <p class="card-subtitle">Entre com suas credenciais para acessar</p>
        
        <div class="form-container">
          <div class="form-field">
            <label for="username">Usuário</label>
            <div class="p-input-icon-left w-full">
              <i class="pi pi-user"></i>
              <InputText 
                id="username" 
                v-model="username" 
                class="w-full" 
                placeholder="Digite seu usuário"
                :disabled="loading"
                @keyup.enter="login"
              />
            </div>
          </div>
          
          <div class="form-field">
            <label for="password">Senha</label>
            <div class="p-input-icon-left w-full">
              <i class="pi pi-lock"></i>
              <InputText 
                id="password" 
                v-model="password" 
                type="password"
                class="w-full" 
                placeholder="Digite sua senha"
                :disabled="loading"
                @keyup.enter="login"
              />
            </div>
          </div>
          
          <div class="demo-notice">
            <Message severity="info">
              <div class="message-content">
                <i class="pi pi-info-circle mr-2"></i>
                <div>
                  <b>Ambiente de demonstração:</b> Utilize qualquer usuário e senha.
                </div>
              </div>
            </Message>
          </div>
          
          <Button 
            label="Entrar" 
            icon="pi pi-sign-in" 
            class="w-full login-button" 
            @click="login"
            :loading="loading"
          />
          
          <div class="visitor-login">
            <Button 
              label="Acessar como Visitante" 
              icon="pi pi-eye" 
              text
              @click="loginVisitante"
              :disabled="loading"
            />
          </div>
        </div>
      </div>
      
      <div class="copyright">
        &copy; 2025 ERP Complete - Todos os direitos reservados
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';

const router = useRouter();
const toast = useToast();

const username = ref('admin');
const password = ref('demo123');
const loading = ref(false);

async function login() {
  if (!username.value || !password.value) {
    toast.add({
      severity: 'warn',
      summary: 'Atenção',
      detail: 'Preencha todos os campos',
      life: 3000
    });
    return;
  }
  
  loading.value = true;
  
  try {
    // Simular autenticação
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Armazenar token demo
    localStorage.setItem('auth_token', 'demo_token_2025');
    localStorage.setItem('user_name', username.value);
    
    toast.add({
      severity: 'success',
      summary: 'Bem-vindo',
      detail: 'Login realizado com sucesso',
      life: 3000
    });
    
    // Navegar para dashboard
    router.push('/');
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Erro',
      detail: 'Falha ao realizar login',
      life: 3000
    });
  } finally {
    loading.value = false;
  }
}

async function loginVisitante() {
  username.value = 'visitante';
  password.value = 'visitante';
  await login();
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f9fafb 0%, #e5e7eb 100%);
  padding: 1rem;
}

.login-container {
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeIn 0.5s ease-in-out;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
}

.logo-img {
  width: 64px;
  height: 64px;
  margin-bottom: 1rem;
}

.app-name {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1E293B;
  margin: 0;
}

.app-version {
  color: #64748B;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.login-card {
  width: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.07);
  padding: 2rem;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1E293B;
  margin: 0 0 0.5rem 0;
  text-align: center;
}

.card-subtitle {
  font-size: 0.875rem;
  color: #64748B;
  margin: 0 0 2rem 0;
  text-align: center;
}

.form-container {
  width: 100%;
}

.form-field {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #334155;
  font-size: 0.875rem;
}

.demo-notice {
  margin: 1.5rem 0;
}

.message-content {
  display: flex;
  align-items: center;
}

.login-button {
  margin-top: 0.5rem;
  height: 2.75rem;
}

.visitor-login {
  margin-top: 1rem;
  text-align: center;
}

.copyright {
  margin-top: 2rem;
  color: #64748B;
  font-size: 0.75rem;
  text-align: center;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 480px) {
  .login-card {
    padding: 1.5rem;
  }
  
  .card-title {
    font-size: 1.25rem;
  }
}
</style>