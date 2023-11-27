/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ["./src/components/EntryPage.vue", "./src/components/LoginPage.vue", "./src/components/ManageAccount.vue", "./src/components/PostingPage.vue", "./src/components/SignupComponent.vue", "./src/components/BusinessInfo.vue", "./src/components/DarkModeSwitch.vue", "./public/index.html"],
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

