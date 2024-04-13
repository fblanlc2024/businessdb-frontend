import Cookies from 'js-cookie';
import { createRouter, createWebHistory } from 'vue-router';
import BusinessInfo from '../components/Pages/BusinessInfo.vue';
import ClientLookup from '../components/Pages/ClientLookup.vue';
import EntryPage from '../components/Pages/EntryPage.vue';
import ManageAccount from '../components/Pages/ManageAccount.vue';
import EventBus from '../components/utils/eventBus';
import { store } from '../main';

const routes = [
  { path: '/', name: 'EntryPage', component: EntryPage },
  { path: '/posting', name: 'ClientLookup', component: ClientLookup, meta: { requiresAuth: true } },
  { path: '/manageAccount', name: 'ManageAccount', component: ManageAccount, meta: { requiresAuth: true } },
  { path: '/businessinfo', name: 'BusinessInfo', component: BusinessInfo, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// If authenticated, go to the route. If not, go to the home route.
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.accounts.isAuthenticated;
  const isGoogleLoginInProgress = Cookies.get('logged_in');
  console.log("isAuthenticated:", isAuthenticated);
  console.log("Navigating to:", to.path);

  if ((isAuthenticated || isGoogleLoginInProgress) && to.path === '/') {
    console.log("Authenticated and navigating to root, redirecting to /posting");
    next('/posting');
    return;
  }

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
  console.log("EventBus handler for token-refresh-failed triggered.");
  console.log("Current isAuthenticated state before update:", store.state.accounts.isAuthenticated);

  store.commit('accounts/setAuthentication', false);

  console.log("Updated isAuthenticated state:", store.state.accounts.isAuthenticated);

  if (router.currentRoute.value.path !== '/') {
    console.log("Redirecting to root due to token refresh failure...");
    router.push('/').catch(err => {
      console.error("Error during redirection to root:", err);
    });
  } else {
    console.log("Already at root. No redirection needed.");
  }
});

export default router;