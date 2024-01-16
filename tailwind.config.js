/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ["./src/components/EntryPage.vue",
  "./src/components/ManageAccount.vue",
  "./src/components/PostingPage.vue",
  "./src/components/BusinessInfo.vue",
  "./src/components/Forms/BusinessForm.vue",
  "./src/components/Forms/LoginComponent.vue",
  "./src/components/Forms/Address Components/AddressLookup.vue",
  "./src/components/Forms/Login Form Components/ForgotPasswordForm.vue",
  "./src/components/Forms/Login Form Components/GoogleLogin.vue",
  "./src/components/Forms/Login Form Components/RegularLogin.vue",
  "./src/components/Forms/Login Form Components/SignUpForm.vue",
  "./src/components/UI Enhancements/DarkModeSwitch.vue",
  "./src/components/Data Display/Info Table Components/MapDisplay.vue",
  "./src/components/Data Display/Info Table Components/PrintReport.vue",
  "./src/components/Data Display/Info Table Components/TableDisplay.vue",
  "./src/components/Data Display/Info Table Components/EditBusinessButton.vue",
  "./src/components/Data Display/Info Table Components/AddressModal.vue",
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

