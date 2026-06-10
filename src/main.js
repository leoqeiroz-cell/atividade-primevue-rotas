import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import 'primeicons/primeicons.css';
import './styles.css';

import App from './App.vue';
import router from './router';
import { pinia } from './store';
import ToastService from 'primevue/toastservice';

createApp(App)
  .use(pinia)
  .use(PrimeVue, {
    theme: {
      preset: Aura,
      options: {
        darkModeSelector: '.app-dark',
      },
    },
  })
  .use(ToastService)
  .use(router)
  .mount('#app');
