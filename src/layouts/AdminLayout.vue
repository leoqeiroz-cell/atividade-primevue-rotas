<script setup>
import Breadcrumb from 'primevue/breadcrumb';
import Button from 'primevue/button';
import Menu from 'primevue/menu';
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const adminMenu = [
  {
    label: 'Gestao',
    items: [
      {
        label: 'Produtos',
        icon: 'pi pi-box',
        command: () => router.push({ name: 'admin-products' }),
      },
      {
        label: 'Relatorios',
        icon: 'pi pi-chart-line',
        command: () => router.push({ name: 'admin-reports' }),
      },
    ],
  },
  {
    label: 'Navegacao',
    items: [
      {
        label: 'Voltar para vitrine',
        icon: 'pi pi-home',
        command: () => router.push({ name: 'home' }),
      },
    ],
  },
];

const breadcrumbItems = computed(() =>
  route.matched
    .filter((record) => record.meta?.breadcrumb)
    .map((record) => ({
      label: record.meta.breadcrumb,
      route: record.path,
    })),
);

function handleLogout() {
  authStore.logout();
  router.push({ name: 'login' });
}
</script>

<template>
  <div class="min-h-screen bg-zinc-100">
    <aside
      class="fixed inset-y-0 left-0 hidden w-72 border-r border-zinc-200 bg-zinc-950 p-5 text-white lg:block"
    >
      <div class="mb-8 flex items-center gap-3">
        <span class="grid h-10 w-10 place-items-center rounded-lg bg-mint text-zinc-950">
          <i class="pi pi-chart-bar" />
        </span>
        <div>
          <p class="font-bold">Admin PrimeShop</p>
          <p class="text-xs text-zinc-400">Bastidores da loja</p>
        </div>
      </div>

      <Menu :model="adminMenu" class="border-0 bg-zinc-900 text-sm" />
    </aside>

    <div class="lg:pl-72">
      <header class="border-b border-zinc-200 bg-white px-4 py-4 lg:px-8">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p class="text-sm text-zinc-500">Bom trabalho por aqui</p>
            <h1 class="text-2xl font-bold text-zinc-900">Painel da equipe</h1>
          </div>

          <div class="flex items-center gap-3">
            <span class="rounded-lg bg-zinc-100 px-3 py-2 text-sm text-zinc-700">
              {{ authStore.user?.name }}
            </span>
            <Button label="Sair" icon="pi pi-sign-out" severity="secondary" outlined @click="handleLogout" />
          </div>
        </div>
      </header>

      <main class="px-4 py-6 lg:px-8">
        <Breadcrumb :model="breadcrumbItems" class="mb-5 border-zinc-200 bg-white">
          <template #item="{ item }">
            <RouterLink
              v-if="item.route"
              :to="item.route"
              class="text-sm font-medium text-zinc-600 hover:text-brand"
            >
              {{ item.label }}
            </RouterLink>
            <span v-else>{{ item.label }}</span>
          </template>
        </Breadcrumb>

        <div class="mb-5 block lg:hidden">
          <Menu :model="adminMenu" class="border-zinc-200 bg-white" />
        </div>

        <RouterView />
      </main>
    </div>
  </div>
</template>
