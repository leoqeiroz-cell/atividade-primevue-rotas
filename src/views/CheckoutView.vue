<script setup>
import Button from 'primevue/button';
import Card from 'primevue/card';
import Divider from 'primevue/divider';
import { useAuthStore } from '../store/auth';
import { cartState, cartTotal, clearCart } from '../store/cart';

const authStore = useAuthStore();

const currency = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
});
</script>

<template>
  <Card class="border border-slate-200 shadow-sm">
    <template #title>Quase tudo pronto</template>
    <template #subtitle>
      Conferimos sua sessao antes de mostrar esta etapa, para manter a compra no lugar certo.
    </template>

    <template #content>
      <div class="grid gap-6 lg:grid-cols-[1fr_280px]">
        <section>
          <div class="rounded-lg bg-emerald-50 p-4 text-sm text-emerald-800">
            Pedido reservado para <strong>{{ authStore.user?.name }}</strong>. Pode revisar com calma.
          </div>

          <Divider />

          <div v-if="cartState.items.length" class="space-y-3">
            <div
              v-for="item in cartState.items"
              :key="item.id"
              class="flex items-center justify-between rounded-lg border border-slate-200 p-4"
            >
              <div>
                <p class="font-medium text-ink">{{ item.name }}</p>
                <p class="text-sm text-slate-500">Quantidade: {{ item.quantity }}</p>
              </div>
              <p class="font-semibold">{{ currency.format(item.price * item.quantity) }}</p>
            </div>
          </div>

          <div v-else class="rounded-lg border border-dashed border-slate-300 p-6 text-slate-500">
            Sua sacola esta vazia. Volte para a vitrine e escolha algo que faca sentido para o seu setup.
          </div>
        </section>

        <section class="rounded-lg bg-slate-50 p-5">
          <p class="text-sm text-slate-500">Total para confirmar</p>
          <p class="mt-1 text-3xl font-bold text-ink">{{ currency.format(cartTotal) }}</p>
          <Button
            label="Confirmar com seguranca"
            icon="pi pi-check"
            severity="success"
            class="mt-5 w-full"
            :disabled="!cartState.items.length"
            @click="clearCart"
          />
        </section>
      </div>
    </template>
  </Card>
</template>
