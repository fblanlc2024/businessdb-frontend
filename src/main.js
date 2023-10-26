import { createApp } from 'vue';
import { createStore } from 'vuex';
import App from './App.vue';
import router from './router';
import './index.css';
import accounts from '@/store/accounts.js';

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
