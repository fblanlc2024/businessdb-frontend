/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ["./src/components/EntryPage.vue", "./src/components/ManageAccount.vue", "./src/components/PostingPage.vue", "./src/components/BusinessInfo.vue", "./src/components/DarkModeSwitch.vue", "./src/components/Forms/BusinessForm.vue",
  "./src/components/Forms/LoginComponent.vue", "./src/components/Forms/Login Form Components/ForgotPasswordForm.vue", "./src/components/Forms/Login Form Components/GoogleLogin.vue", "./src/components/Forms/Login Form Components/RegularLogin.vue", "./src/components/Forms/Login Form Components/SignUpForm.vue",
  './src/components/Forms/Business Form Components/AddBusinessButton.vue', './src/components/Forms/Business Form Components/BusinessName.vue', './src/components/Forms/Business Form Components/ContactInfo.vue', './src/components/Forms/Business Form Components/HasAvailableResources.vue', './src/components/Forms/Business Form Components/OrganizationType.vue', './src/components/Forms/Business Form Components/ResourcesAvailable.vue',
  "./public/index.html"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
  corePlugins: {
    preflight: true
  }
}

