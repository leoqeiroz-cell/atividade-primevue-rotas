<script setup>
import Menubar from 'primevue/menubar';
import Button from 'primevue/button';
import Badge from 'primevue/badge';
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';
import { cartCount } from '../store/cart';

const router = useRouter();
const authStore = useAuthStore();

const menuItems = computed(() => [
  {
    label: 'Vitrine',
    icon: 'pi pi-home',
    command: () => router.push({ name: 'home' }),
  },
  {
    label: 'Checkout',
    icon: 'pi pi-shopping-bag',
    command: () => router.push({ name: 'checkout' }),
  },
  {
    label: 'Admin',
    icon: 'pi pi-shield',
    command: () => router.push({ name: 'admin-products' }),
  },
]);

function handleAuthClick() {
  if (authStore.isAuthenticated) {
    authStore.logout();
    router.push({ name: 'login' });
    return;
  }

  router.push({ name: 'login' });
}
</script>

<template>
  <header class="border-b border-slate-200 bg-white">
    <div class="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-4 lg:px-8">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <RouterLink to="/" class="flex items-center gap-3">
          <span class="grid h-10 w-10 place-items-center rounded-lg bg-brand text-white">
            <i class="pi pi-bolt" />
          </span>
          <div>
            <p class="text-lg font-bold text-ink">PrimeShop</p>
            <p class="text-xs text-slate-500">Tecnologia escolhida com cuidado</p>
          </div>
        </RouterLink>

        <div class="flex items-center gap-3">
          <div class="hidden text-right text-sm sm:block">
            <p class="font-medium text-slate-700">
              {{ authStore.user?.name || 'Visitante' }}
            </p>
            <p class="text-xs text-slate-500">
              {{ authStore.user?.role === 'ADMIN' ? 'Equipe da loja' : authStore.user?.role ? 'Cliente logado' : 'Navegando sem login' }}
            </p>
          </div>
          <div class="relative">
            <Button icon="pi pi-shopping-cart" rounded text aria-label="Carrinho" />
            <Badge
              v-if="cartCount"
              :value="cartCount"
              severity="info"
              class="absolute -right-1 -top-1"
            />
          </div>
          <Button
            :label="authStore.isAuthenticated ? 'Sair' : 'Entrar'"
            :icon="authStore.isAuthenticated ? 'pi pi-sign-out' : 'pi pi-sign-in'"
            severity="secondary"
            outlined
            @click="handleAuthClick"
          />
        </div>
      </div>

      <Menubar :model="menuItems" class="border-slate-200 bg-slate-50" />
    </div>
  </header>
</template>
