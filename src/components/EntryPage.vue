<template>
  <DarkModeSwitch></DarkModeSwitch>
  <div>
    <input v-model="userMessage" @keyup.enter="sendMessage" placeholder="Type your message here">
    <button @click="sendMessage(userMessage)">Send</button>
    <button @click="startRecording">start recording</button>
    <button @click="stopRecording">stop recording</button>
    <div v-if="aiResponse">
      <p>AI Response: {{ aiResponse }}</p>
      <audio ref="audioPlayer" display="none"></audio>
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
import { io } from "socket.io-client";
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
    const socket = io('https://localhost:5000'); 
    const aiResponse = ref('');
    const audioChunks = ref([]);
    const mediaRecorder = ref(null);
    const audioRecorder = ref(null);
    const isRecording = ref(false);
    const audioPlayer = ref(null);
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    // let source = null;

    socket.on('stream_chunk', (data) => {
      if (data.content) {
        aiResponse.value += data.content;
      }
    });

    const sendMessage = (userMessage) => {
      if(userMessage != null)
      {
        socket.emit('text-generator', { message: userMessage });
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

    const startRecording = async () => {
      console.log("Start recording button clicked");
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const options = { mimeType: 'audio/webm' };
        const mediaRecorder = new MediaRecorder(stream, options);

        mediaRecorder.ondataavailable = event => {
          // Send audio chunks to the server in real-time
          const reader = new FileReader();
          reader.onloadend = () => {
            const base64data = reader.result;
            console.log("Sending audio chunk to server");
            socket.emit('audio_data', { data: base64data });
          };
          reader.readAsDataURL(event.data);
        };

        // Start recording with a timeslice of 1000 ms
        mediaRecorder.start(1000);  // Timeslice set to 1000 milliseconds
        
        // Save the MediaRecorder to stop it later
        audioRecorder.value = mediaRecorder;
        isRecording.value = true;
        console.log("MediaRecorder started");
      } catch (error) {
        console.error("Error in starting MediaRecorder:", error);
      }
    };

    const stopRecording = () => {
      console.log("Stop recording button clicked");
      if (audioRecorder.value && isRecording.value) {
        audioRecorder.value.stop();
        console.log("MediaRecorder stopped");
        isRecording.value = false;
        socket.emit('end_audio_stream')
      }
    };

    socket.on('transcription_result', (data) => {
          if (data.transcript) {
            aiResponse.value = data.transcript; // Update aiResponse with the transcribed text
          }
        });

        socket.on('tts_stream_full', (data) => {
        const audioData = data.audio_data;
        // Convert base64 to Blob and then create an audio URL
        const audioBlob = base64ToBlob(audioData, 'audio/mp3'); // Adjust MIME type if needed
        const audioUrl = URL.createObjectURL(audioBlob);

        // Play the audio
        audioPlayer.value.src = audioUrl;
        audioPlayer.value.play().catch(e => console.error("Error playing audio:", e));
    });

    const base64ToBlob = (base64, mimeType) => {
        const byteCharacters = atob(base64);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        return new Blob([byteArray], { type: mimeType });
    }


    return {
      redirectToLogin,
      isOpen,
      openModal,
      closeModal,
      userMessage,
      aiResponse,
      sendMessage,
      audioChunks,
      startRecording,
      stopRecording,
      audioPlayer,
      mediaRecorder,
      audioRecorder,
      audioContext,
      base64ToBlob
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