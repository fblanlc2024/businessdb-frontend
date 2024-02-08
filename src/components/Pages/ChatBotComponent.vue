<template>
  <div class="flex">
    <div id="main-content">
      <!-- <input v-model="userMessage" @keyup.enter="sendMessage" placeholder="Type your message here">
      <button @click="sendMessage(userMessage)">Send</button>
      <button @click="startRecording">start recording</button>
      <button @click="stopRecording">stop recording</button> -->
      <!-- <input v-model="assistantInput" @keyup.enter="sendToAssistant" placeholder="Type your message here to send to assistant">
      <button @click="sendToAssistant">Send to assistant</button> -->
      <!-- <div>
        <div v-if="assistantResponse">
          <p>assistant response: {{ assistantResponse }}</p>
        </div>
        <div v-if="aiResponse">
          <p>AI Response: {{ aiResponse }}</p>
          <audio ref="audioPlayer" display="none"></audio>
        </div>
      </div> -->
      <div v-if="selectedThread">
        <div v-for="message in selectedMessages" :key="message.id">
          <p>{{ message.role }}: {{ message.text }}</p>
        </div>
      </div>
      
    </div>

  <!-- Navigation Toggle - TailwindCSS -->
  <button 
    @click="toggleElements" 
    type="button" 
    class="nav-toggle-button"
    :style="{ left: chevronPosition + 'px' }"
    aria-label="Toggle navigation"
  >
    <!-- Chevron icons -->
    <span v-if="isSidebarOpen" class="icon-wrapper">
      <ChevronLeftIcon class="icon" />
    </span>
    <span v-else class="icon-wrapper">
      <ChevronRightIcon class="icon" />
    </span>
  </button>
  <!-- End Navigation Toggle -->

  <div id="docs-sidebar" class="hs-overlay hs-overlay-open:translate-x-0 -translate-x-full transition-all duration-300 transform fixed top-0 start-0 bottom-0 z-[60] w-64 bg-white border-e border-gray-200 pt-7 pb-10 overflow-y-auto overflow-x-hidden lg:block lg:translate-x-0 lg:end-auto lg:bottom-0 [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-track]:bg-gray-100 [&::-webkit-scrollbar-thumb]:bg-gray-300 dark:[&::-webkit-scrollbar-track]:bg-slate-700 dark:[&::-webkit-scrollbar-thumb]:bg-slate-500 dark:bg-gray-800 dark:border-gray-700">
    <div class="px-6">
      <button @click="newSelection" class="flex-none text-xl font-semibold dark:text-white">
        New chat
      </button>
    </div>

    <nav class="w-full px-2 flex flex-col flex-wrap">
      <div class="w-full overflow-hidden transition-[height] duration-300">
        <ul>
          <li>
            <div
              v-for="thread in threads"
              :key="thread.thread_id"
              @click="selectThread(thread.thread_id)"
            >
              <button
                type="button"
                class="w-full text-start flex items-center gap-x-4 py-2 px-4 text-sm text-slate-700 rounded-lg hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-900 dark:text-slate-400 dark:hover:text-slate-300"
                :class="{ 'selected-thread': thread.thread_id === selectedThread }"
              >
                <ChatBubbleLeftIcon class="w-4 h-4" />
                {{ thread.title }}
              </button>
            </div>
          </li>
        </ul>
      </div>
    </nav>
  </div>

  <div id="chatbox" class="flex justify-center items-center h-screen overflow-x-hidden">
        <div class="absolute bottom-0 left-1/2 transform -translate-x-1/2 flex flex-row items-center h-16 rounded-xl bg-white w-2/5 px-4">
          <!-- Search Icon -->
          <div>
                <button class="flex items-center justify-center text-gray-400 hover:text-gray-600">
                  <svg
                          class="w-5 h-5"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"
                          ></path>
                        </svg>
                </button>
              </div>
              <!-- Input Field -->
              <div class="flex-grow ml-4">
                <div class="relative w-full">
                  <input v-model="assistantInput" @keyup.enter="sendToAssistant" placeholder="Type your message here to send to assistant" type="text" class="flex w-full border rounded-xl focus:outline-none focus:border-indigo-300 pl-4 h-10" />
                  <button class="absolute flex items-center justify-center h-full w-12 right-0 top-0 text-gray-400 hover:text-gray-600">
                    <svg
                            class="w-6 h-6"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                            ></path>
                          </svg>
                  </button>
                </div>
              </div>
              <!-- Send Button -->
              <div class="ml-4">
                <button @click="sendToAssistant" class="flex items-center justify-center bg-indigo-500 hover:bg-indigo-600 rounded-xl text-white px-4 py-1 flex-shrink-0">
                  <span>Send</span>
                  <span class="ml-2">
                    <svg
                            class="w-4 h-4 transform rotate-45 -mt-px"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                            ></path>
                          </svg>
                  </span>
                </button>
              </div>
            </div>
          </div>
  </div>

  <!-- <div v-for="thread in threads" :key="thread.metadata.uuid" @click="selectThread(thread.metadata.uuid)">
    <p>{{ thread.title }}</p>
  </div> -->
</template>
  
<script>
import { ChatBubbleLeftIcon, ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/24/outline';
import axios from 'axios';
import { io } from "socket.io-client";
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

  export default {
    components: {
      ChevronLeftIcon,
      ChevronRightIcon,
      ChatBubbleLeftIcon
    },
    setup() {
      const store = useStore();
      const router = useRouter();
      const userMessage = ref('');
      const socket = io('https://localhost:5000'); 
      const aiResponse = ref('');
      const audioChunks = ref([]);
      const mediaRecorder = ref(null);
      const audioRecorder = ref(null);
      const isRecording = ref(false);
      const audioPlayer = ref(null);
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const assistantInput = ref('');
      const assistantResponse = ref('');
      const threads = ref([]);
      const selectedThread = ref(null);
      const selectedThreadId = ref(null);
      const selectedMessages = ref([]);
      const isSidebarOpen = ref(true);
      const chevronPosition = ref(0);
      const userId = computed(() => store.getters['accounts/getUserId']);

      const toggleElements = () => {
        const sidebarElement = document.getElementById('docs-sidebar');
        const mainContentElement = document.getElementById('main-content');
        const chatboxElement = document.getElementById('chatbox');

        if (!sidebarElement || !mainContentElement || !chatboxElement) {
          console.error("Elements not found");
          return;
        }

        sidebarElement.classList.toggle('off-canvas');
        isSidebarOpen.value = !isSidebarOpen.value;

        // Adjust the chevron and main content position
        chevronPosition.value = isSidebarOpen.value ? sidebarElement.offsetWidth : 0;
        mainContentElement.style.transform = `translateX(${isSidebarOpen.value ? sidebarElement.offsetWidth + 'px' : '0'})`;

        // Adjust the chatbox horizontal position
        const chatboxNewLeft = isSidebarOpen.value ? sidebarElement.offsetWidth * 1/2 : 0;
        chatboxElement.style.left = `calc(50% + ${chatboxNewLeft}px)`;
      };

      onMounted(() => {
        fetchUserThreads();
        const sidebarElement = document.getElementById('docs-sidebar');
        const mainContentElement = document.getElementById('main-content');

        if (sidebarElement && mainContentElement) {
          // Set the initial chevron position based on the initial state of the sidebar
          chevronPosition.value = isSidebarOpen.value ? sidebarElement.offsetWidth : 0;

          // Adjust the main content position based on the initial state of the sidebar
          mainContentElement.style.transform = `translateX(${isSidebarOpen.value ? sidebarElement.offsetWidth + 'px' : '0'})`;
        }
      });

      const sendToAssistant = async () => {
        if (!assistantInput.value) return;

        let tempThreadId = selectedThread.value;

        // If no thread is selected, create a temporary one
        if (!tempThreadId) {
          tempThreadId = 'temp_' + Date.now();
          threads.value.push({
            title: 'New chat',
            thread_id: tempThreadId, // Temporary ID
            messages: [{ role: 'user', text: assistantInput.value }]
          });
          selectedThread.value = tempThreadId;
          selectedMessages.value = [{ role: 'user', text: assistantInput.value }];
        } else {
          // Add the user's message to the selected thread
          const threadIndex = threads.value.findIndex(t => t.thread_id === tempThreadId);
          if (threadIndex !== -1) {
            threads.value[threadIndex].messages.push({ role: 'user', text: assistantInput.value });
          }
        }

        // Emit assistant-request with the thread ID or null for a new thread
        socket.emit('assistant-request', {
          user_id: userId.value,
          message: assistantInput.value,
          thread_id: tempThreadId.startsWith('temp_') ? null : tempThreadId
        });

        assistantInput.value = '';
      };

      const newSelection = () => {
        selectedMessages.value = null;
        selectedThread.value = null;
      }

      socket.on('stream_chunk', (data) => {
        if (data.content) {
          aiResponse.value += data.content;
        }
      });

      socket.on('assistant-response', async (data) => {
        if (data.content) {
          // Check if this is an update for a temporary thread or a new thread creation
          if (data.thread_id && data.thread_id.startsWith('temp_')) {
            // Find the temporary thread in your threads array
            let tempThreadIndex = threads.value.findIndex(t => t.thread_id === data.thread_id);
            
            if (tempThreadIndex !== -1) {
              // If found, update the temporary thread with the new data
              threads.value[tempThreadIndex].title = data.title || "New Chat"; // Use the title from data if available
              threads.value[tempThreadIndex].thread_id = data.thread_id; // Update with the new thread_id from the backend
              threads.value[tempThreadIndex].messages.push({ role: 'assistant', text: data.content });
            }
          } else if (data.thread_id) {
            // Handling for non-temporary thread updates or new threads
            let threadIndex = threads.value.findIndex(t => t.thread_id === data.thread_id);

            if (threadIndex !== -1) {
              // Existing thread found, just push the new message
              threads.value[threadIndex].messages.push({ role: 'assistant', text: data.content });
            } else {
              // This is genuinely a new thread (not replacing a temp one)
              const newThread = {
                title: data.title || "New Chat", // Use the title from data if available
                thread_id: data.thread_id,
                messages: [{ role: 'assistant', text: data.content }]
              };
              threads.value.push(newThread);
              threadIndex = threads.value.length - 1;
            }
          }

          // Update the selected thread if it matches the thread_id in the response
          if (selectedThread.value === data.thread_id || !selectedThread.value) {
            selectedThread.value = data.thread_id;
            selectedMessages.value = threads.value.find(t => t.thread_id === data.thread_id).messages;
          }

          // Optionally, refetch threads to ensure UI is up-to-date
          await fetchUserThreads(); // Consider if necessary, as this may not be needed if you're already updating the state
          await selectThread(data.thread_id); // May not be needed if already updating the state above
        }
      });

  
      const sendMessage = (userMessage) => {
        if(userMessage != null)
        {
          socket.emit('text-generator', { message: userMessage });
        }
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

      const fetchUserThreads = async () => {
        try {
          const response = await axios.get(`https://localhost:5000/get-user-threads/${userId.value}`, {withCredentials: true});
          threads.value = response.data;
          console.log("the threads value: ", threads.value)
        } catch (error) {
          console.error("Error fetching user threads:", error);
        }
      };

      const selectThread = async (thread_id) => {
        selectedThread.value = thread_id;
        const thread = threads.value.find(t => t.thread_id === thread_id);

        if (thread && !thread.messages) {
          try {
            const response = await axios.get(`https://localhost:5000/load-messages/${thread_id}`);
            thread.messages = response.data; // Store messages in the thread
            selectedMessages.value = response.data;
          } catch (error) {
            console.error("Error fetching messages for thread:", error);
          }
        } else if (thread && thread.messages) {
          selectedMessages.value = thread.messages; // Use existing messages if already present
        }
      };

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
        base64ToBlob,
        userId,
        assistantInput,
        sendToAssistant,
        assistantResponse,
        fetchUserThreads,
        selectThread,
        threads,
        store,
        router,
        selectedThread,
        selectedMessages,
        toggleElements,
        isSidebarOpen,
        chevronPosition,
        selectedThreadId,
        newSelection
      };
    }
  }
</script>
  
<style scoped>
#main-content {
  transition: transform 0.3s ease-in-out;
}

#docs-sidebar {
  transition: transform 0.3s ease-in-out;
  transform: translateX(0);
}

#docs-sidebar.off-canvas {
  transform: translateX(-100%);
}

#chatbox {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 100%;
  transition: left 0.3s ease-in-out; /* Smooth transition for left property */
}

body {
  overflow-x: hidden; /* Prevent horizontal scrolling on the body */
}


.nav-toggle-button {
  position: fixed;
  top: 50%;
  transition: left 0.3s ease-in-out;
  z-index: 20;
  left: 0;
}

.nav-toggle-button.toggle-open {
  left: calc(100% - 64px);
}

.icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 25px; /* Adjust as needed */
  height: 25px; /* Adjust as needed */
}

.selected-thread {
  background-color: #d1d5db; /* Gray color, adjust as needed */
}

</style>
