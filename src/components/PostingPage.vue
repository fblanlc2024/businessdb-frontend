<template>
  <div>
    <h1 @click="redirectToManagement">Welcome, {{ username }} ({{ userId }})!</h1>
    <button @click="logOut">Log out</button>
  </div>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import api from '../api.js';

export default {
name: 'PostingPage',
setup() {
  const store = useStore();
  const router = useRouter();

  const userId = computed(() => store.getters['accounts/getUserId']);
  const username = computed(() => store.getters['accounts/getUsername']);

  const redirectToManagement = () => {
    router.push({
      name: 'ManageAccount'
    });
  };

  const fetchCurrentUser = () => {
    const csrf_access = store.state.accounts.access_csrf;

    if (!csrf_access) {
        // console.error('Access CSRF token is missing.');
        fetchUserFromGoogleSession();
        return;
    }

    api.get('/protected', {
        headers: {
            'X-CSRF-TOKEN': csrf_access
        },
        withCredentials: true
    })
    .then(response => {
        const { data } = response;
        store.dispatch('accounts/setUserCredentials', {
            id: data.id,
            username: data.logged_in_as,
        });
        console.log("Updated store state with JWT user data:", store.state.accounts);
    })
    .catch(error => {
        console.error('Error fetching current user:', error);
    });
  };


  const fetchUserFromGoogleSession = () => {
  console.log("Fetching Google session user...");

  api.get('/google_user_data', {
    withCredentials: true
  })
  .then(response => {
      const { data } = response;
      const loggedIn = Cookies.get('logged_in');
      store.dispatch('accounts/setUserCredentials', {
        id: data.account_id,
        username: data.account_name,
        isAuthenticated: true
      });
      Cookies.remove(loggedIn);
      console.log("Updated store state with Google user data:", store.state.accounts);
    })
    .catch(error => {
      console.error('Error fetching Google session user:', error);
    });
  };

  const logOut = () => {
  axios.post('https://localhost:5000/logout', {}, { withCredentials: true })
    .then(response => {
      console.log(response.data.message);
      store.dispatch('accounts/logOut');
      router.push('/');
    })
    .catch(error => {
      console.error('Logout failed:', error);
    });
}


  onMounted(() => {
    fetchCurrentUser();
  });

  return {
    userId,
    username,
    api,
    redirectToManagement,
    logOut,
    fetchCurrentUser,
    fetchUserFromGoogleSession
  };
}
};
</script>