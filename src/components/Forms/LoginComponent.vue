<template>
  <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
      <h2 v-if="!showSignup && !showForgotPassword" class="mt-10 text-center text-2xl font-mono-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
      <h2 v-if="showSignup" class="mt-10 text-center text-2xl font-mono-bold leading-9 tracking-tight text-gray-900">Sign up for an account</h2>
      <h2 v-if="showForgotPassword" class="mt-10 text-center text-2xl font-mono-bold leading-9 tracking-tight text-gray-900">Forgot Password</h2>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <!-- Login Form -->
      <RegularLogin></RegularLogin>

      <!-- Signup Form -->
      <SignUpForm></SignUpForm>

      <!-- Forgot Password Form -->
      <ForgotPasswordForm></ForgotPasswordForm>

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
import { provide, ref } from 'vue';
import ForgotPasswordForm from './Login Form Components/ForgotPasswordForm.vue';
import RegularLogin from './Login Form Components/RegularLogin.vue';
import SignUpForm from './Login Form Components/SignUpForm.vue';

export default {
  name: 'SignupComponent',
  components: {
    RegularLogin,
    SignUpForm,
    ForgotPasswordForm
  },
  setup() {
    const showSignup = ref(false);
    const showForgotPassword = ref(false);

    provide('showSignup', showSignup);
    provide('showForgotPassword', showForgotPassword);
    provide('showSignup', showSignup);

    return {
      showSignup,
      showForgotPassword
    };
  }
};
</script>