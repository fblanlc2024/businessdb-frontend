<template>
  <header class="sticky top-0 inset-x-0 -mt-12 flex flex-wrap sm:justify-start sm:flex-nowrap z-40 bg-white text-sm  dark:bg-gray-800">
    <nav class="max-w-full w-full mx-auto px-4 sm:flex sm:items-center sm:justify-between" aria-label="Global">
      <div class="flex items-center justify-between">
        <a class="flex-none" href="#">
          <img class="w-10 h-auto rounded-md" src="@/assets/sakura_logo.png" alt="Logo">
        </a>
        <div class="sm:hidden">
          <button type="button" class="hs-collapse-toggle p-2 inline-flex justify-center items-center gap-x-2 rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-transparent dark:border-gray-700 dark:text-white dark:hover:bg-white/10 dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600" data-hs-collapse="#navbar-image-1" aria-controls="navbar-image-1" aria-label="Toggle navigation">
            <svg class="hs-collapse-open:hidden flex-shrink-0 w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" x2="21" y1="6" y2="6"/><line x1="3" x2="21" y1="12" y2="12"/><line x1="3" x2="21" y1="18" y2="18"/></svg>
            <svg class="hs-collapse-open:block hidden flex-shrink-0 w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
          </button>
        </div>
      </div>
      <div id="navbar-image-1" class="hs-collapse hidden overflow-hidden transition-all duration-300 basis-full grow sm:block">
        <div class="flex flex-col gap-5 mt-5 sm:flex-row sm:items-center sm:justify-end sm:mt-0 sm:ps-5">
          <a
            class="font-medium cursor-pointer"
            :class="{'text-blue-500': activeLink === 'Lookup', 'text-gray-600 hover:text-gray-400 dark:text-gray-400 dark:hover:text-gray-500': activeLink !== 'Lookup'}"
            aria-current="page"
            @click.prevent="setActiveLink('Lookup'), redirectToPage('PostingPage')"
          >Lookup</a>

          <a
            class="font-medium cursor-pointer"
            :class="{'text-blue-500': activeLink === 'Settings', 'text-gray-600 hover:text-gray-400 dark:text-gray-400 dark:hover:text-gray-500': activeLink !== 'Settings'}"
            @click.prevent="setActiveLink('Settings'), redirectToPage('ManageAccount')"
          >Settings</a>

          <h1 v-if="headerText" class="absolute left-1/2 transform -translate-x-1/2 -translate-y-1/2 sm:translate-y-0 top-1/2 sm:top-auto w-auto text-2xl font-bold mt-0.25">
            {{ headerText }}
          </h1>
          <button @click="logOut()" class="ml-1 inline-flex items-center px-4 py-0.5 mt-0.5 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
            Log out
          </button>
          <DarkModeSwitch class="mt-10"></DarkModeSwitch>
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import EventBus from '../utils/eventBus';
import DarkModeSwitch from './DarkModeSwitch.vue';

export default {
  components: {
    DarkModeSwitch
  },
  setup() {
    const activeLink = ref('');
    const store = useStore();
    const router = useRouter();
    const route = useRoute();

    const setActiveLink = (name) => {
      activeLink.value = name;
    }

    const redirectToPage = (pageName) => {
      if (route.name !== pageName) {
        router.push({
          name: pageName
        });
      }
    };

    const headerText = computed(() => {
      if (route.name === 'PostingPage') {
        return 'Client Lookup';
      }
      if (route.name === 'ManageAccount') {
        return 'Manage Account';
      }
      return '';
    });

    const logOut = () => {
        axios.post('https://localhost:5000/logout', {}, { withCredentials: true })
            .then(response => {
            console.log(response.data.message);
            Cookies.remove('logged_in')
            store.dispatch('accounts/logOut');
            router.push('/');
        })
            .catch(error => {
            console.error('Logout failed:', error);
        });
    };

    onMounted (() => {
      EventBus.on('setActiveLink', setActiveLink);
    })

    onUnmounted (() => {
      EventBus.off('setActiveLink', setActiveLink);
    })

    return {
      activeLink,
      setActiveLink,
      logOut,
      redirectToPage,
      store,
      router,
      route,
      headerText
    };
  },
};

</script>