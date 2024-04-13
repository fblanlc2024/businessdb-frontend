<!-- Sign up form -->

<template>
  <form v-if="showSignup" class="space-y-6" @submit.prevent="handleSignup">
    <div>
        <label for="signupUsername" class="block text-sm font-medium leading-6 text-gray-900">Username</label>
        <div class="mt-2">
            <input id="signupUsername" v-model="signupUsername" required placeholder="Enter username" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
        </div>
    </div>

    <div>
        <label for="signupPassword" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
        <div class="mt-2">
            <input id="signupPassword" v-model="signupPassword" type="password" required placeholder="Enter password" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
        </div>
    </div>

    <div>
        <label for="confirmPassword" class="block text-sm font-medium leading-6 text-gray-900">Confirm Password</label>
        <div class="mt-2">
            <input id="confirmPassword" 
            v-model="confirmPassword" 
            type="password"
            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" 
            required 
            placeholder="Confirm password" />
        </div>
        <p v-if="signupErrMsg" class="text-sm text-red-600 mt-1">{{ signupErrMsg }}</p>
    </div>

    <div class="mt-4">
        <button type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Sign up</button>
    </div>
  </form>
</template>

<script>
import axios from 'axios';
import { inject, ref } from 'vue';

export default {
  name: 'SignUpForm',
  setup() {
    const signupUsername = ref('');
    const signupPassword = ref('');
    const confirmPassword = ref('');
    const signupErrMsg = ref('');
    const showSignup = inject('showSignup');
    const showLogin = inject('showLogin');
    const showForgotPassword = inject('showForgotPassword');

    const handleSignup = () => {
      if (signupPassword.value !== confirmPassword.value) {
        console.error('Passwords do not match.');
        signupErrMsg.value = 'Passwords do not match.'
        return;
      }
      axios.post(`${process.env.VUE_APP_BACKEND_URL}/account`, {
          username: signupUsername.value,
          password: signupPassword.value
      })
      .then(response => {
          if (response.data.message === 'Account created successfully') {
              console.log(response.data.message);
              showLogin.value = true;
              showSignup.value = false
              showForgotPassword.value = false
              signupErrMsg.value = '';
          } else {
            signupErrMsg.value = 'Signup failed. Please try again.';
            console.error('Error signing up:', response.data.message);
          }
      })
      .catch(err => {
          signupErrMsg.value = 'Error signing up. Please check your details.';
          console.error('Error signing up:', err);
      });
    };

    return {
      signupUsername,
      signupPassword,
      confirmPassword,
      handleSignup,
      signupErrMsg,
      showSignup,
      showLogin,
      showForgotPassword
    };
  }
};
</script>

<style></style>