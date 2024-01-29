import Cookies from 'js-cookie';
import { createRouter, createWebHistory } from 'vue-router';
import BusinessInfo from '../components/Pages/BusinessInfo.vue';
import Chatbot from '../components/Pages/ChatBotComponent.vue';
import EntryPage from '../components/Pages/EntryPage.vue';
import ManageAccount from '../components/Pages/ManageAccount.vue';
import PostingPage from '../components/Pages/PostingPage.vue';
import EventBus from '../components/utils/eventBus';
import { store } from '../main';

const routes = [
  { path: '/', name: 'EntryPage', component: EntryPage },
  { path: '/posting', name: 'PostingPage', component: PostingPage, meta: { requiresAuth: true } },
  { path: '/manageAccount', name: 'ManageAccount', component: ManageAccount, meta: { requiresAuth: true } },
  { path: '/businessinfo', name: 'BusinessInfo', component: BusinessInfo, meta: { requiresAuth: true } },
  { path: '/chatbot', name: 'ChatBot', component: Chatbot, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.accounts.isAuthenticated;
  const isGoogleLoginInProgress = Cookies.get('logged_in');
  console.log("isAuthenticated:", isAuthenticated);
  console.log("Navigating to:", to.path);

  // Redirect authenticated users from root to '/posting'
  if ((isAuthenticated || isGoogleLoginInProgress) && to.path === '/') {
    console.log("Authenticated and navigating to root, redirecting to /posting");
    next('/posting');
    return;
  }

  // Redirect unauthenticated users trying to access protected routes to '/'
  if (to.matched.some(record => record.meta.requiresAuth) && (!isAuthenticated && !isGoogleLoginInProgress)) {
    console.log("Unauthenticated access to a protected route, redirecting to root");
    next('/');
    return;
  }

  next();
});

router.afterEach((to, from, failure) => {
  if (!failure) {
    setTimeout(() => {
      if (window.HSStaticMethods) {
        window.HSStaticMethods.autoInit();
      }
    }, 100);
  }
});

EventBus.on('token-refresh-failed', () => {
  console.log("Token refresh failed, redirecting to root...");

  // Update the authentication state in the store
  store.commit('accounts/setAuthentication', false);

  // Redirect to the root if not already there
  if (router.currentRoute.value.path !== '/') {
    router.push('/').catch(err => {
      // Handle the error or log it
      console.error("Router error:", err);
    });
  }
});

export default router;