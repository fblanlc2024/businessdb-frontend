import accounts from '@/store/accounts.js';
import "preline/preline";
import { createApp } from 'vue';
import { createStore } from 'vuex';
import App from './App.vue';
import './index.css';
import router from './router';

const store = createStore({
  modules: {
    accounts
  },
});

export { store };

createApp(App)
  .use(store)
  .use(router)
  .mount('#app');
