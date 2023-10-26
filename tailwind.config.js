/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/App.vue", "./src/components/EntryPage.vue", "./src/components/LoginPage.vue", "./src/components/ManageAccount.vue", "./src/components/PostingPage.vue", "./src/components/SignupComponent.vue"],
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

