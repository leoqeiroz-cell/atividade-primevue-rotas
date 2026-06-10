<script setup>
import Button from 'primevue/button';
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import { computed, reactive, ref } from 'vue';
import useVuelidate from '@vuelidate/core';
import { email, helpers, minLength, required } from '@vuelidate/validators';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import { useAuthStore } from '../store/auth';

const route = useRoute();
const router = useRouter();
const toast = useToast();
const authStore = useAuthStore();

const activeMode = ref('login');

const loginForm = reactive({
  email: '',
  password: '',
});

const registerForm = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
});

const requiredMessage = helpers.withMessage('Campo obrigatorio', required);
const emailMessage = helpers.withMessage('Informe um e-mail valido', email);
const passwordLengthMessage = helpers.withMessage('A senha deve ter no minimo 6 caracteres', minLength(6));
const samePasswordMessage = helpers.withMessage(
  'As senhas nao coincidem',
  (value) => value === registerForm.password,
);

const loginRules = {
  email: { required: requiredMessage, email: emailMessage },
  password: { required: requiredMessage },
};

const registerRules = {
  name: { required: requiredMessage },
  email: { required: requiredMessage, email: emailMessage },
  password: { required: requiredMessage, minLength: passwordLengthMessage },
  confirmPassword: { required: requiredMessage, sameAsPassword: samePasswordMessage },
};

const vLogin$ = useVuelidate(loginRules, loginForm);
const vRegister$ = useVuelidate(registerRules, registerForm);

const redirectTarget = computed(() => route.query.redirect || { name: 'home' });

function fieldError(validator, field) {
  return validator[field].$errors[0]?.$message;
}

function fieldClass(validator, field) {
  return {
    'p-invalid border-red-500': validator[field].$error,
  };
}

async function submitLogin() {
  const isValid = await vLogin$.value.$validate();

  if (!isValid) {
    toast.add({
      severity: 'error',
      summary: 'Validacao pendente',
      detail: 'Revise os campos destacados antes de continuar.',
      life: 3200,
    });
    return;
  }

  try {
    const user = await authStore.login(loginForm);
    toast.add({
      severity: 'success',
      summary: 'Login realizado!',
      detail: `Bem-vindo(a), ${user.name}.`,
      life: 3000,
    });
    router.push(route.query.redirect || (user.role === 'ADMIN' ? { name: 'admin-products' } : { name: 'home' }));
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Credenciais invalidas',
      detail: error.message,
      life: 3500,
    });
  }
}

async function submitRegister() {
  const isValid = await vRegister$.value.$validate();

  if (!isValid) {
    toast.add({
      severity: 'error',
      summary: 'Cadastro incompleto',
      detail: 'Corrija os campos destacados para criar a conta.',
      life: 3200,
    });
    return;
  }

  try {
    const user = await authStore.register(registerForm);
    toast.add({
      severity: 'success',
      summary: 'Conta criada!',
      detail: `Cadastro de ${user.name} concluido com sucesso.`,
      life: 3000,
    });
    router.push(redirectTarget.value);
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Erro no cadastro',
      detail: error.message,
      life: 3500,
    });
  }
}
</script>

<template>
  <Card class="mx-auto max-w-xl border border-slate-200 shadow-sm">
    <template #title>Acesso seguro PrimeShop</template>
    <template #subtitle>Entre com sua conta ou realize um cadastro validado antes de continuar.</template>

    <template #content>
      <div class="mb-6 grid grid-cols-2 rounded-lg border border-slate-200 bg-slate-50 p-1">
        <button
          type="button"
          class="rounded-md px-4 py-2 text-sm font-semibold transition"
          :class="activeMode === 'login' ? 'bg-white text-brand shadow-sm' : 'text-slate-600 hover:text-ink'"
          @click="activeMode = 'login'"
        >
          Login
        </button>
        <button
          type="button"
          class="rounded-md px-4 py-2 text-sm font-semibold transition"
          :class="activeMode === 'register' ? 'bg-white text-brand shadow-sm' : 'text-slate-600 hover:text-ink'"
          @click="activeMode = 'register'"
        >
          Criar conta
        </button>
      </div>

      <form v-if="activeMode === 'login'" class="space-y-4" novalidate @submit.prevent="submitLogin">
        <div>
          <label for="login-email" class="mb-2 block text-sm font-medium text-slate-700">E-mail</label>
          <InputText
            id="login-email"
            v-model.trim="loginForm.email"
            type="email"
            class="w-full"
            :class="fieldClass(vLogin$, 'email')"
            aria-describedby="login-email-error"
            @blur="vLogin$.email.$touch()"
          />
          <p v-if="vLogin$.email.$error" id="login-email-error" class="mt-1 text-sm text-red-600">
            {{ fieldError(vLogin$, 'email') }}
          </p>
        </div>

        <div>
          <label for="login-password" class="mb-2 block text-sm font-medium text-slate-700">Senha</label>
          <Password
            id="login-password"
            v-model="loginForm.password"
            toggleMask
            :feedback="false"
            class="w-full"
            inputClass="w-full"
            :class="fieldClass(vLogin$, 'password')"
            aria-describedby="login-password-error"
            @blur="vLogin$.password.$touch()"
          />
          <p v-if="vLogin$.password.$error" id="login-password-error" class="mt-1 text-sm text-red-600">
            {{ fieldError(vLogin$, 'password') }}
          </p>
        </div>

        <div class="rounded-lg bg-slate-50 p-3 text-sm text-slate-600">
          Cliente: cliente@primeshop.com / 123456<br />
          Admin: admin@primeshop.com / admin123
        </div>

        <Button
          label="Entrar"
          icon="pi pi-sign-in"
          type="submit"
          class="w-full"
          :loading="authStore.isLoading"
          :disabled="vLogin$.$invalid || authStore.isLoading"
        />
      </form>

      <form v-else class="space-y-4" novalidate @submit.prevent="submitRegister">
        <div>
          <label for="register-name" class="mb-2 block text-sm font-medium text-slate-700">Nome</label>
          <InputText
            id="register-name"
            v-model.trim="registerForm.name"
            class="w-full"
            :class="fieldClass(vRegister$, 'name')"
            aria-describedby="register-name-error"
            @blur="vRegister$.name.$touch()"
          />
          <p v-if="vRegister$.name.$error" id="register-name-error" class="mt-1 text-sm text-red-600">
            {{ fieldError(vRegister$, 'name') }}
          </p>
        </div>

        <div>
          <label for="register-email" class="mb-2 block text-sm font-medium text-slate-700">E-mail</label>
          <InputText
            id="register-email"
            v-model.trim="registerForm.email"
            type="email"
            class="w-full"
            :class="fieldClass(vRegister$, 'email')"
            aria-describedby="register-email-error"
            @blur="vRegister$.email.$touch()"
          />
          <p v-if="vRegister$.email.$error" id="register-email-error" class="mt-1 text-sm text-red-600">
            {{ fieldError(vRegister$, 'email') }}
          </p>
        </div>

        <div>
          <label for="register-password" class="mb-2 block text-sm font-medium text-slate-700">Senha</label>
          <Password
            id="register-password"
            v-model="registerForm.password"
            toggleMask
            class="w-full"
            inputClass="w-full"
            :class="fieldClass(vRegister$, 'password')"
            aria-describedby="register-password-error"
            @blur="vRegister$.password.$touch()"
          />
          <p v-if="vRegister$.password.$error" id="register-password-error" class="mt-1 text-sm text-red-600">
            {{ fieldError(vRegister$, 'password') }}
          </p>
        </div>

        <div>
          <label for="register-confirm-password" class="mb-2 block text-sm font-medium text-slate-700">
            Confirmar senha
          </label>
          <Password
            id="register-confirm-password"
            v-model="registerForm.confirmPassword"
            toggleMask
            :feedback="false"
            class="w-full"
            inputClass="w-full"
            :class="fieldClass(vRegister$, 'confirmPassword')"
            aria-describedby="register-confirm-password-error"
            @blur="vRegister$.confirmPassword.$touch()"
          />
          <p
            v-if="vRegister$.confirmPassword.$error"
            id="register-confirm-password-error"
            class="mt-1 text-sm text-red-600"
          >
            {{ fieldError(vRegister$, 'confirmPassword') }}
          </p>
        </div>

        <Button
          label="Criar conta"
          icon="pi pi-user-plus"
          type="submit"
          class="w-full"
          :loading="authStore.isLoading"
          :disabled="vRegister$.$invalid || authStore.isLoading"
        />
      </form>
    </template>

    <template #footer>
      <RouterLink to="/">
        <Button label="Voltar para a vitrine" icon="pi pi-arrow-left" severity="secondary" outlined />
      </RouterLink>
    </template>
  </Card>
</template>
