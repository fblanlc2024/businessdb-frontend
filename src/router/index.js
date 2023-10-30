// import Cookies from 'js-cookie'; // Import js-cookie
import { createRouter, createWebHistory } from 'vue-router';
import EntryPage from '../components/EntryPage.vue';
import ManageAccount from '../components/ManageAccount.vue';
import PostingPage from '../components/PostingPage.vue';
// import EventBus from '../eventBus';
// import { store } from '../main';

const routes = [
  { path: '/', name: 'EntryPage', component: EntryPage },
  { path: '/posting', name: 'PostingPage', component: PostingPage, meta: { requiresAuth: true } },
  { path: '/manageAccount', name: 'ManageAccount', component: ManageAccount, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// router.beforeEach((to, from, next) => {
//   const isAuthenticated = store.state.accounts.isAuthenticated;
//   console.log("isAuthenticated:", isAuthenticated);
//   console.log("Navigating to:", to.path);

//   // If the user is authenticated and tries to visit the root path, redirect to '/posting'
//   if (isAuthenticated && to.path === '/') {
//     next('/posting');
//     return;
//   }

//   // Check if the route requires authentication
//   if (to.matched.some(record => record.meta.requiresAuth)) {
//     if (!isAuthenticated) {
//       // Redirect to the entry page if not authenticated
//       next({ path: '/' });
//     } else {
//       // Check if the access token is present and valid
//       const accessToken = Cookies.get('access_token_cookie');
//       if (!accessToken) {
//         // If the access token is missing, attempt to refresh it
//         EventBus.emit('refresh-token-needed');
//         next(false); // Cancel the navigation
//       } else {
//         next(); // Allow access if the user is authenticated and token is present
//       }
//     }
//   } else {
//     next(); // Allow access by default
//   }
// });

// // Listen to the token-refresh-failed event from the EventBus
// EventBus.on('token-refresh-failed', () => {
//   store.commit('accounts/setAuthentication', false);
//   if (router.currentRoute.value.path !== '/') {
//     router.push('/');
//   }
// });

// // Listen to the refresh-token-needed event from the EventBus
// EventBus.on('refresh-token-needed', () => {
//   // Implement the logic to refresh the token here
//   // For example, you could dispatch an action from your Vuex store
//   store.dispatch('accounts/refreshToken')
//     .then(() => {
//       // If the token is refreshed successfully, retry the original navigation
//       router.push(router.currentRoute.value.fullPath);
//     })
//     .catch(() => {
//       // If the token refresh fails, redirect to the login page
//       router.push('/');
//     });
// });

export default router;