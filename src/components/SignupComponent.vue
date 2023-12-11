<template>
  <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
      <h2 v-if="!showSignup && !showForgotPassword" class="mt-10 text-center text-2xl font-mono-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
      <h2 v-if="showSignup" class="mt-10 text-center text-2xl font-mono-bold leading-9 tracking-tight text-gray-900">Sign up for an account</h2>
      <h2 v-if="showForgotPassword" class="mt-10 text-center text-2xl font-mono-bold leading-9 tracking-tight text-gray-900">Forgot Password</h2>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <!-- Login Form -->
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
        <p class="or font-mono-bold mt-6"><span>Or Continue With</span></p>

        <div class="flex items-center justify-center mt-6 space-x-4 gap-2">
          <button type="button" @click="redirectToGoogleAuth" class="bg-red-500 p-2 font-semibold text-white inline-flex items-center space-x-2 rounded">
            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="w-5" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><g fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 0C5.372 0 0 5.373 0 12s5.372 12 12 12c6.627 0 12-5.373 12-12S18.627 0 12 0zm.14 19.018c-3.868 0-7-3.14-7-7.018c0-3.878 3.132-7.018 7-7.018c1.89 0 3.47.697 4.682 1.829l-1.974 1.978v-.004c-.735-.702-1.667-1.062-2.708-1.062c-2.31 0-4.187 1.956-4.187 4.273c0 2.315 1.877 4.277 4.187 4.277c2.096 0 3.522-1.202 3.816-2.852H12.14v-2.737h6.585c.088.47.135.96.135 1.474c0 4.01-2.677 6.86-6.72 6.86z" fill="currentColor"/></g></svg>
          </button>
        </div>
      </form>

      <!-- Signup Form -->
      <form v-if="showSignup" class="space-y-6" @submit.prevent="handleSignup">
        <!-- Username -->
        <div>
          <label for="signupUsername" class="block text-sm font-medium leading-6 text-gray-900">Username</label>
          <div class="mt-2">
            <input id="signupUsername" v-model="signupUsername" required placeholder="Enter username" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
          </div>
        </div>

        <!-- Password -->
        <div>
          <label for="signupPassword" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
          <div class="mt-2">
            <input id="signupPassword" v-model="signupPassword" type="password" required placeholder="Enter password" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
          </div>
        </div>

        <!-- Confirm Password -->
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

        <!-- Signup Button -->
        <div class="mt-4">
          <button type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Sign up</button>
        </div>
      </form>

      <!-- Forgot Password Form -->
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


      <!-- Toggle between Login and Signup -->
      <p class="mt-8 text-center text-sm text-gray-500">
        <template v-if="showForgotPassword">
            <a href="#" @click.prevent="showForgotPassword = false" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">I do not want to change my password.</a>
        </template>
        <template v-else-if="!showSignup">
            Not a member?
            <a href="#" @click.prevent="showSignup = true" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">Sign up!</a>
        </template>
        <template v-else>
            Already a member?
            <a href="#" @click.prevent="showSignup = false" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">Sign in!</a>
        </template>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

export default {
  name: 'SignupComponent',
  setup() {
    const showSignup = ref(false);
    const router = useRouter();
    const store = useStore();

    const loginUsername = ref('');
    const loginPassword = ref('');

    const signupUsername = ref('');
    const signupPassword = ref('');
    const confirmPassword = ref('');

    const showForgotPassword = ref(false);

    const loginErrMsg = ref('');
    const signupErrMsg = ref('');
    const forgotPasswordErrMsg = ref('');
    const confirmedNewPassword = ref('');
    const remainingAttempts = ref(5);
    const remainingMinutes = ref(15);

    const googleOAuthEndpoint = 'https://localhost:5000/login';

    const handleLogin = () => {
      loginUser(loginUsername.value, loginPassword.value)
      .then(response => {
          console.log('Backend response:', response.data);
          // console.log("Response Headers:", response.headers);

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

    const handleSignup = () => {
      if (signupPassword.value !== confirmPassword.value) {
        console.error('Passwords do not match.');
        signupErrMsg.value = 'Passwords do not match.'
        return;
      }
      axios.post('https://localhost:5000/account', {
          username: signupUsername.value,
          password: signupPassword.value
      })
      .then(response => {
          if (response.data.message === 'Account created successfully') {
              console.log(response.data.message);
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

    const redirectToGoogleAuth = () => {
      store.commit('accounts/setGoogleLogin', true);
      window.location.href = googleOAuthEndpoint;
    };


    const handleForgotPassword = () => {
      // Check if passwords match
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
          showForgotPassword.value = false;  // Hide the forgot password form
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
      showSignup,
      loginUsername,
      loginPassword,
      signupUsername,
      signupPassword,
      confirmPassword,
      handleLogin,
      handleSignup,
      loginUser,
      redirectToPageTwo,
      redirectToGoogleAuth,
      handleForgotPassword,
      showForgotPassword,
      loginErrMsg,
      signupErrMsg,
      forgotPasswordErrMsg,
      confirmedNewPassword,
      remainingAttempts,
      remainingMinutes
    };
  }
};
</script>

<style scoped>
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
