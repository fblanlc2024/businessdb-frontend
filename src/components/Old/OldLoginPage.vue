<template>
    <div>
      <div>
        <button @click="showSignup = false">Login</button>
        <button @click="showSignup = true">Signup</button>
        <button @click="redirectToGoogleAuth">Login with Google</button>
      </div>
  
      <!-- Login div -->
      <div v-show="!showSignup">
        <h2>Login</h2>
        <input v-model="loginUsername" placeholder="Username" />
        <input type="password" v-model="loginPassword" placeholder="Password" />
        <button @click="handleLogin">Login</button>
        <div v-show="loginErrMsg">
          Invalid username or password. Please try again.
        </div>
      </div>
  
      <!-- Signup div -->
      <div v-show="showSignup">
        <h2>Signup</h2>
        <input v-model="signupUsername" placeholder="Username" />
        <input type="password" v-model="signupPassword" placeholder="Password" />
        <input type="password" v-model="confirmPassword" placeholder="Confirm Password" />
        <button @click="handleSignup">Signup</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

  export default {
    name: 'LoginForm',
    setup() {
      var showSignup = ref(false);
      var loginErrMsg = ref(false);
      var router = useRouter();
      var store = useStore();

      var loginUsername = ref('');
      var loginPassword = ref('');
  
      var signupUsername = ref('');
      var signupPassword = ref('');
      var confirmPassword = ref('');

      const googleOAuthEndpoint = 'http://localhost:5000/login';

      var redirectToPageTwo = () => {
          router.push({
            name: 'ClientLookup'
          });
      };

      

      function loginUser(username, password) {
          return axios.get('http://localhost:5000/account', {
              params: {
                  username: username,
                  password: password
              }
          });
      }

      var handleLogin = () => {
          loginUser(loginUsername.value, loginPassword.value)
          .then(response => {
              if (response.data.message === 'Login successful') {
                  store.dispatch('accounts/setUserCredentials', {
                      id: response.data.user._id,
                      username: response.data.user.username
                  });

                  console.log("Vuex Store State:", store.state.accounts);
                  redirectToPageTwo();
              } else {
                  loginErrMsg.value = true;
              }
          })
          .catch(err => {
              loginErrMsg.value = true;
              console.error('Login error:', err);
          });
      };

      const redirectToGoogleAuth = () => {
        window.location.href = googleOAuthEndpoint;
      };
  
      var handleSignup = () => {
          if (signupPassword.value != confirmPassword.value) {
              console.error('Passwords do not match.');
              return;
          }

          axios.post('http://localhost:5000/account', {
              username: signupUsername.value,
              password: signupPassword.value
          })
          .then(response => {
              if (response.data.message === 'Account created successfully') {
                  console.log(response.data.message);
              } else {
                  console.error('Error signing up:', response.data.message);
              }
          })
          .catch(err => {
              console.error('Error signing up:', err);
          });
      };

      return {
        showSignup,
        loginUsername,
        loginPassword,
        signupUsername,
        signupPassword,
        confirmPassword,
        loginErrMsg,
        handleLogin,
        handleSignup,
        redirectToGoogleAuth
      };
    }
  };
  </script>