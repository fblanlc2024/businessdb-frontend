<template>
  <form v-if="!showSignup && !showForgotPassword" class="space-y-6" @submit.prevent="handleLogin">
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
            <a href="#" @click.prevent="showForgotPassword = true" class="font-semibold text-indigo-600 hover:text-indigo-500">Forgot password?</a>
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

    <!-- Login Button -->
    <div>
      <button type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Sign in</button>
    </div>
      <p class="or font-mono-bold mt-6"><span>Or</span></p>
    <div>
      <GoogleLogin></GoogleLogin>
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
    const showForgotPassword = inject('showForgotPassword');
    const showSignup = inject('showSignup');

    const handleLogin = () => {
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
          }
      })
      .catch(err => {
        if (err.response) {
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
          name: 'PostingPage'
        });
    };

    function loginUser(username, password) {
        return axios.post('https://localhost:5000/token_login_set', {
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
      showSignup
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
</style>