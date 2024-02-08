<template>
    <NavbarComponent />
    <div class="mx-4 mt-16 min-h-screen max-w-screen-xl sm:mx-8 xl:mx-auto">
        <div class="col-span-8 overflow-hidden rounded-xl sm:bg-gray-50 sm:px-8 sm:shadow dark:bg-gray-900">
          <div class="pt-4">
            <h1 class="py-2 text-2xl font-semibold">Account settings</h1>
          </div>
          <hr class="mt-4 mb-8" />
          <p class="py-2 text-xl font-semibold">Username</p>
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <p v-show="showDelete || !showUpdate" class="text-gray-600 dark:text-gray-300">Your username is <strong>{{ username }}</strong></p>
            <button v-show="showDelete || !showUpdate" @click="updateAndDelete('update')" class="text-sm font-semibold text-blue-600 underline decoration-2 self-end sm:self-auto">Change</button>
            <div v-show="showUpdate" class="mt-4">
              <div class="flex flex-col sm:flex-row sm:space-x-4">
                <div class="flex flex-col sm:w-1/2">
                  <label for="current-username" class="text-sm text-gray-500">Current Username</label>
                  <input type="text" id="current-username" class="mt-1 rounded-md border-2 border-gray-300 py-2 px-4 text-base text-gray-700 placeholder-gray-400 focus:border-blue-600 focus:outline-none" :value="username" disabled />
                </div>
                <div class="flex flex-col sm:w-1/2">
                  <label for="new-username" class="text-sm text-gray-500">New Username</label>
                  <input type="text" id="new-username" v-model="newUsername" class="mt-1 rounded-md border-2 border-gray-300 py-2 px-4 text-base text-gray-700 placeholder-gray-400 focus:border-blue-600 focus:outline-none" placeholder="New Username" />
                </div>
              </div>
              <div class="flex items-center mt-4 space-x-4">
                <button @click="updateAccount" class="rounded-lg bg-blue-600 hover:bg-blue-500 px-4 py-2 text-white">Save Username</button>
                <button @click="cancelUsernameChange" class="rounded-lg bg-gray-500 hover:bg-gray-400 px-4 py-2 text-white">Cancel</button>
                <div v-if="usernameErrMsg" class="text-sm font-medium text-red-600">
                  {{ usernameErrMsg }}
                </div>
              </div>
            </div>
            <hr class="mt-4 mb-8" />
          </div>
          <hr class="mt-4 mb-8" />
          <p class="py-2 text-xl font-semibold">Password</p>
          <div class="flex items-center">
            <div class="flex flex-col space-y-2 sm:flex-row sm:space-y-0 sm:space-x-3">
              <label for="login-password">
                <span class="text-sm text-gray-500">Current Password</span>
                <div class="relative flex overflow-hidden rounded-md border-2 transition focus-within:border-blue-600">
                  <input :disabled="isUsernameActive" :type="isVisible ? 'text' : 'password'" v-model="currentPassword" id="login-password" class="w-full flex-shrink appearance-none border-gray-300 bg-white py-2 px-4 text-base text-gray-700 placeholder-gray-400 focus:outline-none" placeholder="***********" />
                </div>
              </label>
              <label for="login-password">
                <span class="text-sm text-gray-500">New Password</span>
                <div class="relative flex overflow-hidden rounded-md border-2 transition focus-within:border-blue-600">
                  <input :disabled="isUsernameActive" :type="isVisible ? 'text' : 'password'" v-model="newPassword" id="login-password" class="w-full flex-shrink appearance-none border-gray-300 bg-white py-2 px-4 text-base text-gray-700 placeholder-gray-400 focus:outline-none" placeholder="***********" />
                </div>
              </label>
            </div>
              <template v-if="isVisible">
                <svg :disabled="isUsernameActive" @click="toggleVisibility" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 mt-6 ml-3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                </svg>
              </template>
              <template v-else>
                <svg :disabled="isUsernameActive" @click="toggleVisibility" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 mt-6 ml-3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                </svg>
              </template>
          </div>
          <div class="flex items-center mt-4 space-x-4">
            <button :disabled="isUsernameActive" @click="updateAccount" class="rounded-lg bg-blue-600 px-4 py-2 text-white">Save Password</button>
            <div v-if="passwordErrMsg" class="text-sm font-medium text-red-600">
              {{ passwordErrMsg }}
            </div>
          </div>
          <hr class="mt-4 mb-8" />

          <div class="mb-10">
            <p class="py-2 text-xl font-semibold">Delete Account</p>
            <p class="inline-flex items-center rounded-full bg-rose-100 px-4 py-1 text-rose-600">
              <svg xmlns="http://www.w3.org/2000/svg" class="mr-2 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              Proceed with caution
            </p>
            <p class="mt-2">Make sure to back up your data! After deletion, you cannot recover your account.</p>
            <button @click="deleteAccount()" class="ml-auto text-sm font-semibold text-rose-600 underline decoration-2">Continue with deletion</button>
          </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import NavbarComponent from '../UI Enhancements/NavbarComponent.vue';
import EventBus from '../utils/eventBus';

export default {
    name: 'ManageAccount',
    components: {
    NavbarComponent
},
    setup() {
      const store = useStore();
      const router = useRouter();
      const showUpdate = ref(false);
      const showDelete = ref(false);
      const newUsername = ref('');
      const currentPassword = ref('');
      const newPassword = ref('');
      const isVisible = ref(false);
      const usernameErrMsg = ref('');
      const passwordErrMsg = ref('');
      const deletionErrMsg = ref('');
      const isUsernameActive = ref(false);
      const activeLink = ref('Lookup');

      const userId = computed(() => store.getters['accounts/getUserId']);
      const username = computed(() => store.getters['accounts/getUsername']);

      const updateAndDelete = (action) => {
        if(action == 'update') {
            showUpdate.value = true;
            showDelete.value = false;
            isUsernameActive.value = true;
        } else {
            showUpdate.value = false;
            showDelete.value = true;
        }
      }

      const cancelUsernameChange = () => {
        showUpdate.value = false;
        isUsernameActive.value = false;
        newUsername.value = '';
      };

      const redirectToLogin = () => {
        router.push({
          name: 'EntryPage'
        });
      }

      const updateAccount = () => {
        usernameErrMsg.value = '';
        passwordErrMsg.value = '';

        if(isUsernameActive.value == true && newUsername.value.trim() == '') {
          usernameErrMsg.value = 'Please enter a valid new username';
          return;
        }

        axios.put('https://localhost:5000/account', {
            username: username.value,
            password: currentPassword.value,
            new_username: newUsername.value,
            new_password: newPassword.value
        },
        {
          withCredentials: true
        })
        .then(response => {
            console.log(response.data);
            store.commit('accounts/setUsername', newUsername.value);
            isUsernameActive.value = false;
            redirectToLogin();
        })
        .catch(err => {
            if (err.response) {
                const error = err.response.data.message;
                console.error('Error updating account:', error);
                if(error.includes('password')) {
                  passwordErrMsg.value = error;
                }
                else if(error.includes('Google')) {
                  if(newUsername.value != '') {
                    usernameErrMsg.value = error;
                  }
                  else {
                    passwordErrMsg.value = error;
                  }
                }
            } else {
                console.error('Error:', err.message);
            }
        });
    }

    const deleteAccount = () => {
        deletionErrMsg.value = '';
        axios.delete('https://localhost:5000/account', {
          data: { username: username.value },
          withCredentials: true
        })
        .then(response => {
            console.log(response.data);
            deletionErrMsg.value = '';
            redirectToLogin();
        })
        .catch(err => {
            console.error('Error deleting account:', err);
            const error = err.response.data.message;
            if(error.includes('Google')) {
              deletionErrMsg.value = error;
              alert(deletionErrMsg.value);
            } else {
              deletionErrMsg.value = 'Failed to delete account. Please try again later.';
            }
        });
    }

    const toggleVisibility = () => {
      isVisible.value = !isVisible.value;
    }

    onMounted(() => {
      EventBus.emit('setActiveLink', 'Settings');
      document.body.classList.add('overflow-hidden');
    });

    onUnmounted(() => {
      document.body.classList.remove('overflow-hidden');
    });

      return {
        userId,
        username,
        newUsername,
        newPassword,
        showUpdate,
        showDelete,
        isVisible,
        currentPassword,
        usernameErrMsg,
        passwordErrMsg,
        deletionErrMsg,
        activeLink,
        isUsernameActive,
        updateAndDelete,
        updateAccount,
        deleteAccount,
        redirectToLogin,
        toggleVisibility,
        cancelUsernameChange
      };
    }
};
</script>