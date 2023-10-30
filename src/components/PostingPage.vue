<template>
  <div>
    <h1 @click="redirectToManagement">Welcome, {{ username }} ({{ userId }})!</h1>
    <button @click="logOut">Log out</button>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
// import axios from 'axios';
// import Cookies from 'js-cookie';
import api from '../api.js';

export default {
name: 'PageTwo',
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
        console.error('Access CSRF token is missing.');
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
        // Only update the user's ID and username, not the CSRF tokens
        store.dispatch('accounts/setUserCredentials', {
            id: data.id,
            username: data.logged_in_as,
            // Do not overwrite the CSRF tokens here
        });
        console.log("Updated store state with JWT user data:", store.state.accounts);
    })
    .catch(error => {
        console.error('Error fetching current user:', error);
        // logOut(); //Taken care of by the router guard.
    });
  };


  // Method to fetch user data from Google session
  const fetchUserFromGoogleSession = () => {
    console.log("Fetching Google session user...");

    api.get('/google_user_data', {
      withCredentials: true
    })
    .then(response => {
      const { data } = response;
      // Update the Vuex store with the user's credentials
      store.dispatch('accounts/setUserCredentials', {
          id: data.account_id,
          username: data.account_name,
          isAuthenticated: true
      });
      console.log("Updated store state with Google user data:", store.state.accounts);
    })
    .catch(error => {
      console.error('Error fetching Google session user:', error);
      // If the error is due to an expired token, the interceptor should handle the refresh.
      // If the refresh fails or there's another error, handle it accordingly.
    });
  };


  const logOut = () => {
    store.dispatch('accounts/logOut');
    router.push('/');
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