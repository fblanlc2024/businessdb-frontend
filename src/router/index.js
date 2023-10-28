import store from '@/store/accounts.js';
import { createRouter, createWebHistory } from 'vue-router';
import EntryPage from '../components/EntryPage.vue';
import ManageAccount from '../components/ManageAccount.vue';
import PostingPage from '../components/PostingPage.vue';
import EventBus from '../eventBus'; // Import the EventBus

const routes = [
  { path: '/', name: 'EntryPage', component: EntryPage },
  { path:  '/posting', name: 'PostingPage', component: PostingPage, meta: { requiresAuth: true } },
  { path: '/manageAccount', name: 'ManageAccount', component: ManageAccount, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.isAuthenticated; // Get the authentication status from the Vuex store

  // If the user is authenticated and tries to visit the root, redirect to /posting
  if (isAuthenticated && to.path === '/') {
    next('/posting');
    return;
  }

  // Check if the route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // Check if the user is not authenticated
    if (!isAuthenticated) {
      if (to.path !== '/') { // Prevent infinite loop by checking if the user is already on the login page
        next({ path: '/' }); // Redirect to LoginPage
      } else {
        next(); // Allow access if the user is already on the login page
      }
    } else {
      next(); // Allow access if the user is authenticated
    }
  } else {
    next(); // Allow access by default
  }
});

// Listen to the token-refresh-failed event from the EventBus
EventBus.on('token-refresh-failed', () => {
    store.commit('accounts/setAuthentication', false);
    if (router.currentRoute.value.path !== '/') {
        router.push('/');
    }
});

export default router;
