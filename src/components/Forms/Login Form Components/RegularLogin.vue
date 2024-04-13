<!-- Regular Login with custom error handling for rate limits, incorrect login attempts -->

<template>
  <form v-if="showLogin" class="space-y-6" @submit.prevent="handleLogin">
    <!-- Username -->
    <div>
        <label for="loginUsername" class="block text-sm font-medium leading-6 text-gray-900">Username</label>
        <div class="mt-2">
        <input id="loginUsername" 
            v-model="loginUsername" 
            name="username" 
            type="text"
            autocomplete="off"
            class="block w-full rounded-md border-0 py-1.5 px-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" 
            required 
            placeholder="Enter username" />
        </div>
    </div>

    <!-- Password -->
    <div>
        <div class="flex items-center justify-between">
        <label for="loginPassword" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
        <div class="text-sm">
            <a href="#" @click.prevent="showForgotPassword = true, showLogin = false, showSignup = false" class="font-semibold text-indigo-600 hover:text-indigo-500">Forgot password?</a>
        </div>
        </div>
        <div class="mt-2">
        <input id="loginPassword" 
            v-model="loginPassword" 
            type="password"
            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" 
            required 
            placeholder="Enter password" />
        </div>
        <p v-if="loginErrMsg" class="text-sm text-red-600 mt-1">{{ loginErrMsg }}</p>
    </div>
    <div>
      <div>
        <button type="submit" :disabled="isLoggingIn" :class="{'flex w-full justify-center rounded-md px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600': true, 'bg-indigo-600 hover:bg-indigo-500': !isLoggingIn, 'bg-indigo-500': isLoggingIn}">
          <div v-if="isLoggingIn" role="status" class="flex items-center justify-center">
            <svg aria-hidden="true" class="w-4 h-4 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
            </svg>
            <span class="sr-only">Loading...</span>
          </div>
          <span v-else>Sign in</span>
        </button>
      </div>
      <div class="relative my-8">
        <div class="absolute inset-0 flex items-center" aria-hidden="true">
          <div class="w-full border-t border-gray-300 dark:border-gray-600"></div>
        </div>
        <div class="relative flex justify-center">
          <span class="bg-white dark:bg-gray-800 px-2 text-sm text-gray-500 dark:text-gray-400">Or</span>
        </div>
      </div>
        <GoogleLogin class="-mt-4"></GoogleLogin>
      </div>
  </form>
</template>

<script>
import axios from 'axios';
import { inject, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import GoogleLogin from './GoogleLogin.vue';

export default {
  name: 'RegularLogin',
  components: {
    GoogleLogin
  },
  setup() {
    const router = useRouter();
    const store = useStore();
    const loginUsername = ref('');
    const loginPassword = ref('');
    const loginErrMsg = ref('');
    const remainingAttempts = ref(5);
    const remainingMinutes = ref(15);
    const isLoggingIn = ref(false);
    const showForgotPassword = inject('showForgotPassword');
    const showSignup = inject('showSignup');
    const showLogin = inject('showLogin');

    const handleLogin = () => {
      isLoggingIn.value = true;
      loginUser(loginUsername.value, loginPassword.value)
      .then(response => {
          console.log('Backend response:', response.data);

          if (response.data.message === 'Login successful') {
              const userId = response.data.user._id;
              const username = response.data.user.username;
              const access_csrf = response.data.csrf_tokens.access_csrf;
              const refresh_csrf = response.data.csrf_tokens.refresh_csrf;

              console.log("Received user ID:", userId);
              console.log("Received username:", username);
              console.log("Recieved Access CSRF", access_csrf);
              console.log("Recieved Refresh CSRF", refresh_csrf);

              store.dispatch('accounts/setUserCredentials', {
                  id: userId,
                  username: username,
                  access_csrf: access_csrf,
                  refresh_csrf: refresh_csrf,
                  isAuthenticated: true
              });

              console.log("Updated Vuex Store State:", store.state.accounts);
              redirectToPageTwo();
              loginErrMsg.value = '';
              remainingAttempts.value = 5;
          } else {
              loginErrMsg.value = 'Login failed. Please try again.';
              isLoggingIn.value = false;
          }
      })
      .catch(err => {
        if (err.response) {
          isLoggingIn.value = false;
          if (err.response.status === 429) {
            if (err.response.data.wait_minutes !== undefined) {
              // Rate limit exceeded for login attempts
              loginErrMsg.value = `Too many login attempts. Please wait for ${err.response.data.wait_minutes} minutes until your next login attempt.`;
            } else {
              // Rate limit exceeded for IP
              loginErrMsg.value = 'You have been temporarily locked out of this application. Please wait before trying to log in again.';
              alert('You have exceeded the login attempts that you can put on this application. Please wait and try again later.');
            }
          } else {
            // Handle other errors including incorrect login details
            if (err.response.data.remaining_attempts !== undefined) {
              remainingAttempts.value = err.response.data.remaining_attempts;
              loginErrMsg.value = 'Incorrect username or password. ' + `Attempts left: ${remainingAttempts.value}`;
            } 
          }
        } else {
          loginErrMsg.value = 'It seems there is an error with our servers. Please try again later.';
        }
        console.error('Login error:', err);
      });
    };

    const redirectToPageTwo = () => {
        router.push({
          name: 'ClientLookup'
        });
    };

    function loginUser(username, password) {
        return axios.post(`${process.env.VUE_APP_BACKEND_URL}/token_login_set`, {
            username: username,
            password: password
        }, {
            withCredentials: true
        });
    }


    return {
      loginUsername,
      loginPassword,
      handleLogin,
      loginUser,
      redirectToPageTwo,
      loginErrMsg,
      remainingAttempts,
      remainingMinutes,
      showForgotPassword,
      showSignup,
      showLogin,
      isLoggingIn
    };
  }
};
</script>

<style>
.or {
text-align: center;
font-weight: normal;
border-bottom: 2px solid rgb(245 239 239);
line-height: 0.1em;
margin: 25px 0;
}
.or span {
background: #fff;
padding: 0 10px;
color: gray;
}

.dark .or span {
  background: #1f2937;
}
</style>