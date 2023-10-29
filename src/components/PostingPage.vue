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
import Cookies from 'js-cookie';
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
        // Handle this situation, e.g., log the user out or show an error message.
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


  const fetchUserFromGoogleSession = () => {
    console.log("gollogolol session!");
    // Extract values from the cookies
    const username = Cookies.get('username');
    const id = Cookies.get('id');
    const jwtToken = Cookies.get('jwt_token_google');

    // Log the extracted values for debugging
    console.log('Extracted from cookies:', {username, id, jwtToken});

    if (username && id && jwtToken) {
        // Update the Vuex store with the user's credentials
        store.dispatch('accounts/setUserCredentials', {
            id: id,
            username: username,
            accessToken: jwtToken
        });

    } else {
        console.error('Failed to retrieve user data from cookies.');
        // Redirect or handle the error as needed
        // logOut(); // Uncomment if you want to logout the user in case of an error
    }
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