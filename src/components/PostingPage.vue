<template>
  <div>
    <h1 @click="redirectToManagement">Welcome, {{ username }} ({{ userId }})!</h1>
    <button @click="logOut">Log out</button>
  </div>

  <div>
    <!--  Header and Title -->
    <div class="flex justify-between items-center mb-4 py-5 pb-5 border-b-2 border-gray-400 text-center dark:border-gray-700">
      <div class="flex-1"></div>
      <h1 class="text-4xl font-bold flex-shrink">Policy Walker</h1>
      <div class="flex-1 flex justify-end">
        <Switch
          v-model="isDarkMode"
          :class="isDarkMode ? 'bg-blue-900' : 'bg-blue-700'"
          class="relative inline-flex h-[38px] w-[74px] shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 mr-8"
        >
          <span class="sr-only">Toggle Dark Mode</span>
          <span
            aria-hidden="true"
            :class="isDarkMode ? 'translate-x-9' : 'translate-x-0'"
            class="pointer-events-none inline-block h-[34px] w-[34px] transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out"
          />
        </Switch>
      </div>
    </div>

    <!-- Client search box description -->
    <div class="box-content h-1/4 w-1/2 p-4 border border-gray-300 ml-8 rounded-lg">
      <div class="text-2xl pl-2 font-bold mb-4">Client Lookup</div>
      <div class="pl-2 mb-4 whitespace-pre-line">On this page, enter your client name in the search box below. Then, click your client name to view all of the policies that are available under your company name.</div>
      <input v-model="textInput" type="text" placeholder="Enter client name:" class="w-1/2 ml-2 px-2 py-2 border border-gray-300 dark:bg-gray-800 dark:border-gray-500 rounded-md shadow-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
    </div>
    
    <!-- Initial catalogue of clients, adjusts with autocomplete -->
    <div class="grid grid-cols-4 gap-2 mt-4 px-8 pb-5">
      <div v-for="business in sortedAndFilteredBusinesses" :key="business" @click="redirectToBusinessInfo(business)" class="px-2 py-1 border rounded-md hover:bg-gray-200 dark:hover:bg-gray-500 dark:hover:text-gray-200 cursor-pointer">
  {{ business }}
</div>

    </div>
  </div>
</template>

<script>
import { Switch } from '@headlessui/vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { computed, onMounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import api from '../api.js';

export default {
name: 'PostingPage',
components: {
  Switch
},
setup() {
  const store = useStore();
  const router = useRouter();

  const userId = computed(() => store.getters['accounts/getUserId']);
  const username = computed(() => store.getters['accounts/getUsername']);

  const textInput = ref('');
  const businesses = ref([]);

  const prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const savedDarkMode = window.localStorage.getItem('isDarkMode');
  const initialDarkMode = savedDarkMode !== null ? savedDarkMode === 'true' : prefersDarkMode;

  const isDarkMode = ref(initialDarkMode);

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

  watch(isDarkMode, (newValue) => {
    console.log("isDarkMode changed:", newValue);
    if (newValue) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    // Save to LocalStorage
    window.localStorage.setItem('isDarkMode', newValue.toString());
  });


  onMounted(() => {
    fetchCurrentUser();
    axios.get('https://localhost:5000/api/businesses')
      .then(response => {
        businesses.value = response.data;
      })
      .catch(error => console.error(error));

      const savedDarkMode = window.localStorage.getItem('isDarkMode');
      if (savedDarkMode !== null) {
        isDarkMode.value = savedDarkMode === 'true';
      } else {
        // If no saved setting, use system preference
        const prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        isDarkMode.value = prefersDarkMode;
      }

      // Apply the dark mode class based on isDarkMode value
      if (isDarkMode.value) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
  });

  const sortedAndFilteredBusinesses = computed(() => {
    let sortedBusinesses = [...businesses.value].sort();

    if (!textInput.value) return sortedBusinesses;
    let val = textInput.value.toUpperCase();
    return sortedBusinesses.filter(business => business.toUpperCase().includes(val));
  });

  const redirectToBusinessInfo = (business) => {
    router.push({
      name: 'BusinessInfo',
      query: {
        businessName: business
      }
    })
  }

  return {
    userId,
    username,
    api,
    redirectToManagement,
    logOut,
    fetchCurrentUser,
    fetchUserFromGoogleSession,
    textInput,
    businesses,
    isDarkMode,
    sortedAndFilteredBusinesses,
    redirectToBusinessInfo
  };
}
};
</script>