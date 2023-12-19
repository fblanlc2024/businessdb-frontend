<template>
  <DarkModeSwitch></DarkModeSwitch>
  <div>
    <input v-model="userMessage" @keyup.enter="sendMessage" placeholder="Type your message here">
    <button @click="sendMessage">Send</button>
    <div v-if="aiResponse">
      <p>AI Response: {{ aiResponse }}</p>
    </div>
  </div>

  <div class="flex flex-col justify-center items-center h-screen space-y-4">
    <div class="opacity-0 animate-fadeIn animation-delay-500">
      <h1 class="text-7xl font-mono mb-4">Welcome</h1>
    </div>

    <div class="opacity-0 animate-fadeIn animation-delay-1000">
      <p class="text-lg font-mono mb-4">Please log in to view your school's business clients.</p>
    </div>
    
    <button
      @click="openModal"
      class="opacity-0 animate-fadeIn animation-delay-1500 mt-8 flex justify-center items-center rounded-lg px-3.5 py-2 m-1 overflow-hidden relative group cursor-pointer border-2 font-medium border-indigo-600 text-indigo-600"
    >
      <span class="absolute w-64 h-0 transition-all duration-300 origin-center rotate-45 -translate-x-20 bg-indigo-600 top-1/2 group-hover:h-64 group-hover:-translate-y-32 ease"></span>
      <span class="relative transition duration-300 group-hover:text-white ease">Log In</span>
    </button>

    <TransitionRoot :show="isOpen" as="template">
      <Dialog as="div" @close="closeModal" class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full md:w-[800px] transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all z-40">
              <LoginComponent />
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script>
import { Dialog, DialogPanel, TransitionChild, TransitionRoot } from '@headlessui/vue';
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import LoginComponent from './Forms/LoginComponent.vue';
import DarkModeSwitch from './UI Enhancements/DarkModeSwitch.vue';

export default {
  components: {
    LoginComponent,
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DarkModeSwitch
  },
  setup() {
    const router = useRouter();
    const isOpen = ref(false);
    const userMessage = ref('');
    const aiResponse = ref('');


    const formatMessage = (message) => {
      let formattedMessage = message
        .replace(/ \./g, '.') // Replace ' .' with '.'
        .replace(/ ,/g, ',') // Replace ' ,' with ','
        .replace(/ \?/g, '?') // Replace ' ?' with '?'
        .replace(/ !/g, '!') // Replace ' !' with '!'
        .replace(/ '/g, '\''); // Replace ' '' with '''

      // Remove the last character
      if (formattedMessage.length > 0) {
        formattedMessage = formattedMessage.substring(0, formattedMessage.length - 1);
      }

      return formattedMessage;
    };

    const fetchData = async () => {
      try {
        const response = await axios.post('https://business-chatbot.sethchangcom.workers.dev', {
          message: userMessage.value
        });
        let fullMessage = '';
        
        const chunks = response.data.split('\n');
        for (const chunk of chunks) {
          if (chunk.includes('[DONE]')) {
            break;  // Stop processing when '[DONE]' is found
          }
          const match = chunk.match(/data: (.+)/);
          if (match && match[1]) {
            fullMessage += JSON.parse(match[1]).response; // Accumulate response parts
          }
        }
        
        aiResponse.value = formatMessage(fullMessage); // Format and set the full message
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const sendMessage = () => {
      if (userMessage.value.trim()) {
        fetchData();
        userMessage.value = '';
      }
    };


    const openModal = () => {
      isOpen.value = true;
    };

    const closeModal = () => {
      isOpen.value = false;
    };

    const redirectToLogin = () => {
      router.push({ name: 'LoginPage' });
    };

    return {
      redirectToLogin,
      isOpen,
      openModal,
      closeModal,
      userMessage,
      aiResponse,
      sendMessage,
      formatMessage
    };
  }
}
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-fadeIn {
  animation-name: fadeIn;
  animation-duration: 1.5s;  /* Extended duration */
  animation-fill-mode: forwards;
}

.animation-delay-500 {
  animation-delay: 0.75s;  /* Extended delay for header */
}

.animation-delay-1000 {
  animation-delay: 1.5s;  /* Extended delay for body */
}

.animation-delay-1500 {
  animation-delay: 2.25s;  /* Extended delay for button */
}
</style>