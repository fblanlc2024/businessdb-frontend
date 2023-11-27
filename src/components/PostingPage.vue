<template>
  <div>
    <div class="flex justify-between items-center mb-4 py-5 pb-5 border-b-2 border-gray-400 text-center dark:border-gray-700">
      <div class="flex-1"></div>
      <h1 class="text-4xl font-bold flex-shrink" @click="redirectToManagement">Welcome, {{ username }}!</h1>
      <div class="flex-1 flex justify-end">
        <DarkModeSwitch></DarkModeSwitch>
      </div>
    </div>

    <div class="box-content h-1/4 w-1/2 p-4 border border-gray-300 ml-8 rounded-lg">
      <div class="text-2xl pl-2 font-bold mb-4">Client Lookup</div>
      <div class="pl-2 mb-4 whitespace-pre-line">On this page, enter your client name in the search box below. Then, click your client name to view all of the policies that are available under your company name.</div>
      <input v-model="textInput" type="text" placeholder="Enter client name:" class="w-1/2 ml-2 px-2 py-2 border border-gray-300 dark:bg-gray-800 dark:border-gray-500 rounded-md shadow-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
    </div>
    
    <div class="grid grid-cols-4 gap-2 mt-4 px-8 pb-5">
      <div v-for="business in sortedAndFilteredBusinesses" :key="business" @click="redirectToBusinessInfo(business)" class="px-2 py-1 border rounded-md hover:bg-gray-200 dark:hover:bg-gray-500 dark:hover:text-gray-200 cursor-pointer">
        {{ business }}
      </div>
    </div>
  </div>
  <div>
    <button @click="logOut">Log out</button>
  </div>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import api from '../api.js';
import DarkModeSwitch from './DarkModeSwitch.vue';

export default {
    name: 'PostingPage',
    components: {
      DarkModeSwitch
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
        };

        onMounted(() => {
            fetchCurrentUser();
            axios.get('https://localhost:5000/api/businesses')
                .then(response => {
                businesses.value = response.data;
            })
                .catch(error => console.error(error));
        });

        const sortedAndFilteredBusinesses = computed(() => {
            let sortedBusinesses = [...businesses.value].sort();
            if (!textInput.value)
                return sortedBusinesses;
            let val = textInput.value.toUpperCase();
            return sortedBusinesses.filter(business => business.toUpperCase().includes(val));
        });

        const redirectToBusinessInfo = (business) => {
            router.push({
                name: 'BusinessInfo',
                query: {
                    businessName: business
                }
            });
        };

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

<style scoped></style>