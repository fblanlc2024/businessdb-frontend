<template>
  <div v-if="showForgotPassword" class="sm:mx-auto sm:w-full sm:max-w-sm">
    <form class="space-y-6" @submit.prevent="handleForgotPassword">
      <!-- Username -->
      <div>
          <label for="forgotUsername" class="block text-sm font-medium leading-6 text-gray-900">Username</label>
          <div class="mt-2">
          <input id="forgotUsername" 
              v-model="loginUsername"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" 
              required 
              placeholder="Enter username" />
          </div>
          <p v-if="forgotPasswordErrMsg" class="text-sm text-red-600 mt-1">{{ forgotPasswordErrMsg }}</p>
      </div>

      <!-- New Password -->
      <div>
          <label for="newPassword" class="block text-sm font-medium leading-6 text-gray-900">New Password</label>
          <div class="mt-2">
              <input id="newPassword" v-model="loginPassword" type="password" required placeholder="Enter new password" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
          </div>
      </div>

      <!-- Confirm New Password -->
      <div>
          <label for="confirmNewPassword" class="block text-sm font-medium leading-6 text-gray-900">Confirm New Password</label>
          <div class="mt-2">
              <input id="confirmNewPassword" 
                  v-model="confirmedNewPassword" 
                  type="password"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" 
                  required 
                  placeholder="Confirm new password" />
          </div>
      </div>

      <!-- Update Password Button -->
      <div class="mt-4">
          <button type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Update Password</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import { inject, ref } from 'vue';

export default {
  name: 'SignupComponent',
  setup() {
    const forgotPasswordErrMsg = ref('');
    const loginUsername = ref('');
    const loginPassword = ref('');
    const confirmedNewPassword = ref('');

    const showForgotPassword = inject('showForgotPassword');

    const handleForgotPassword = () => {
      if (loginPassword.value !== confirmedNewPassword.value) {
        console.error('Passwords do not match.');
        forgotPasswordErrMsg.value = 'One or more fields is invalid. Please try again.'
        return;
      }

      axios.put('https://localhost:5000/reset_password', {
        username: loginUsername.value,
        new_password: loginPassword.value
      })
      .then(response => {
        if (response.data.message === 'Password updated successfully') {
          console.log(response.data.message);
          showForgotPassword.value = false;
          forgotPasswordErrMsg.value = '';
        } else {
          forgotPasswordErrMsg.value = 'One or more fields is invalid. Please try again.';
          console.error('Error resetting password:', response.data.message);
        }
      })
      .catch(err => {
        forgotPasswordErrMsg.value = 'No account with this username found.';
        console.error('Error resetting password:', err);
      });
    };


    return {
      loginUsername,
      loginPassword,
      handleForgotPassword,
      forgotPasswordErrMsg,
      confirmedNewPassword,
      showForgotPassword
    };
  }
};
</script>

<style>
</style>