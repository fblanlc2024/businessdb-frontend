<template>
  <button @click="toggleElements" class="fixed bottom-4 right-4 z-50 flex items-center justify-center bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-full">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
      <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.76c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.076-4.076a1.526 1.526 0 0 1 1.037-.443 48.282 48.282 0 0 0 5.68-.494c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
    </svg>
  </button>

  <div id="chat" class="flex flex-col">
    <div id="docs-sidebar" class="hs-overlay transition-all duration-300 transform fixed top-0 end-0 bottom-0 z-50 w-full md:w-1/5 bg-white border-l border-gray-400 dark:bg-gray-800 pt-7 pb-10 md:overflow-hidden overflow-y-auto">
      <div class="px-4 flex items-center">
        <!-- Close button with @click directive for toggleElements method -->
        <button @click="toggleElements" class="dark:text-white -mt-2.5" aria-label="Close sidebar">
          <XMarkIcon class="w-6 h-6" />
        </button>
        <h2 class="flex-1 -mt-1 ml-2 overflow-x-auto nowrap font-semibold">{{ selectedThreadTitle }}</h2>
        <button @click="newSelection" class="flex-none text-xl font-semibold dark:text-white -mt-2">
          <PencilSquareIcon class="w-6 h-6 mr-2" />
        </button>
        <button @click="loadTitlesOnly" aria-label="Load Titles Only" class="text-black dark:text-white -mt-1.5">
          <svg height="21px" version="1.1" viewBox="0 0 20 21" width="20px" xmlns="http://www.w3.org/2000/svg">
            <g fill="currentColor" opacity="0.9">
              <path d="M10.5,0 C7,0 3.9,1.9 2.3,4.8 L0,2.5 L0,9 L6.5,9 L3.7,6.2 C5,3.7 7.5,2 10.5,2 C14.6,2 18,5.4 18,9.5 C18,13.6 14.6,17 10.5,17 C7.2,17 4.5,14.9 3.4,12 L1.3,12 C2.4,16 6.1,19 10.5,19 C15.8,19 20,14.7 20,9.5 C20,4.3 15.7,0 10.5,0 L10.5,0 Z M9,5 L9,10.1 L13.7,12.9 L14.5,11.6 L10.5,9.2 L10.5,5 L9,5 L9,5 Z"/>
            </g>
          </svg>
        </button>
      </div>
      <nav class="w-full flex flex-col overflow-hidden" style="height: calc(100vh - 125px);">
        <div class="px-2 overflow-y-auto">
          <!-- Loop through threads for selection -->
          <ul v-if="titlesShown" class="space-y-1">
            <li v-for="thread in threads" :key="thread.thread_id">
              <button @click="selectThread(thread.thread_id)" type="button" class="w-full text-start flex items-center gap-x-4 py-2 px-4 text-sm text-slate-700 rounded-lg hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-900 dark:text-slate-400 dark:hover:text-slate-300">
                <ChatBubbleLeftIcon class="w-4 h-4" />
                <span class="truncate">{{ thread.title }}</span>
              </button>
            </li>
          </ul>
          <!-- Display selected thread messages -->
          <div v-if="showSplash" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50">
            <div class="text-center">
              <ChatBubbleLeftIcon class="mx-auto w-24 h-24 text-gray-500 dark:text-gray-200" />
              <p class="text-lg text-gray-700 mt-4 dark:text-gray-200">How can I assist you today?</p>
            </div>
          </div>
          <div v-show="selectedThread" class="flex-1 overflow-y-auto break-words" style="max-height: calc(100vh - 125px);">
            <div v-for="message in selectedMessages" :key="message.id" class="message">
              <p>{{ message.role }}: {{ message.text }}</p>
            </div>
          </div>
          <audio ref="audioPlayer" style="display: none;"></audio>
        </div>
      </nav>


      <div id="chatbox" class="pb-4 flex-1 break-words bg-white dark:bg-gray-800">
        <div v-if="uploadedFiles.length > 0" class="flex overflow-x-auto overflow-y-hidden bg-gray-800/70 dark:bg-gray/70 border-b border-gray-300 p-2 mb-2">
          <div v-for="file in uploadedFiles" :key="file.name"
            class="group bg-gray-200 text-gray-800 text-sm leading-5 mx-1 my-1 flex items-center relative px-4 py-2 rounded-full whitespace-nowrap hover:bg-gray-300">
            <DocumentIcon class="w-4 h-4 mr-2"/>
            {{ file.name }}
            <XCircleIcon @click="removeFile(file)" class="w-6 h-6 absolute right-0 top-0 -mr-1.5 -mt-1.5 hidden group-hover:block rounded-full bg-gray-100"/>
          </div>
        </div>
        <div class="flex flex-row items-center h-full rounded-xl bg-white w-full px-4 dark:bg-gray-800">
          <input type="file" ref="fileInput" @change="handleFileSelection" multiple style="display: none;">
          <button @click="triggerFileExplorer" class="flex-none mr-2 -ml-2 dark:text-white">
            <PaperClipIcon class="w-6 h-6"/>
          </button>
          <div class="flex flex-grow items-center border rounded-xl overflow-hidden bg-white dark:bg-gray-800">
            <textarea v-model="assistantInput"
          @keyup.enter.prevent="sendToAssistant"
          @input="autoExpand"
          placeholder="Type here..."
          class="text-area flex-grow focus:outline-none h-auto pl-4 border-none resize-none overflow-hidden dark:bg-gray-800 -ml-0.5"
          rows="1"></textarea>
            <button class="flex items-center justify-center bg-indigo-500 hover:bg-indigo-600 text-white focus:outline-none rounded-full m-1 p-2">
              <MicrophoneIcon @click="startRecording" v-if="!isRecording" class="w-4 h-4"/>
              <StopCircleIcon @click="stopRecording" v-else class="w-4 h-4" />
            </button>
          </div>
          <button @click="sendToAssistant" class="flex-none ml-2 flex items-center justify-center bg-indigo-500 hover:bg-indigo-600 rounded-full text-white p-2 h-8 w-8">
            <PaperAirplaneIcon class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ChatBubbleLeftIcon, DocumentIcon, MicrophoneIcon, PaperAirplaneIcon, PaperClipIcon, PencilSquareIcon, StopCircleIcon, XCircleIcon, XMarkIcon } from '@heroicons/vue/24/outline';
import axios from 'axios';
import { io } from "socket.io-client";
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

  export default {
    components: {
    ChatBubbleLeftIcon,
    XMarkIcon,
    PaperAirplaneIcon,
    PencilSquareIcon,
    PaperClipIcon,
    MicrophoneIcon,
    StopCircleIcon,
    DocumentIcon,
    XCircleIcon,
    // ChatBubbleLeftRightIcon
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
      const showSplash = ref(true);
      const audioPlayer = ref(null);
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const assistantInput = ref('');
      const assistantResponse = ref('');
      const threads = ref([]);
      const selectedThread = ref(null);
      const selectedThreadTitle = ref('');
      const selectedMessages = ref([]);
      const fileInput = ref(null);
      const uploadedFiles = ref([]);
      const isSidebarOpen = ref(false);
      const isCalling = ref(false);
      const titlesShown = ref(false);
      const userId = computed(() => store.getters['accounts/getUserId']);

      const toggleElements = () => {
        const sidebarElement = document.getElementById('docs-sidebar');
        if (!sidebarElement) {
          console.error("Sidebar element not found");
          return;
        }

        sidebarElement.classList.toggle('off-canvas');
        isSidebarOpen.value = !isSidebarOpen.value;
      };

      const loadTitlesOnly = () => {
        selectedMessages.value = null;
        showSplash.value = false;
        selectedThread.value = null;
        selectedThreadTitle.value = '';
        uploadedFiles.value = [];
        titlesShown.value = true;
      };

      onMounted(() => {
        fetchUserThreads();
      });

      const sendToAssistant = async () => {
        if (!assistantInput.value) {
          return;
        }

        let tempThreadId = selectedThread.value;
        const textAreaElement = document.querySelector('.text-area');
        if (textAreaElement) {
          textAreaElement.style.height = 'inherit';
          textAreaElement.style.height = `${textAreaElement.scrollHeight}px`;
          textAreaElement.style.height = '40px';
        }

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

        if (uploadedFiles.value.length > 0) {
          console.log("uploaded files value: ", uploadedFiles.value);
          const promises = uploadedFiles.value.map(file => {
            return new Promise((resolve, reject) => {
              const reader = new FileReader();
              reader.onload = () => {
                const base64Data = reader.result.split(',')[1]; // Remove the data url prefix and get the base64 encoded string
                resolve({
                  name: file.name,
                  content: base64Data,
                  type: file.type,
                  size: file.size
                });
              };
              reader.onerror = reject;
              reader.readAsDataURL(file); // Read the file as Data URL
            });
          });

          try {
            const filesBase64 = await Promise.all(promises);

            // Emit the socket event including the base64 encoded files
            socket.emit('assistant-request', {
              user_id: userId.value,
              message: assistantInput.value,
              thread_id: tempThreadId.startsWith('temp_') ? null : tempThreadId,
              files: filesBase64
            });

          } catch (error) {
            console.error('Error reading files', error);
          }
        } else {
          // If no files, just send the text
          socket.emit('assistant-request', {
            user_id: userId.value,
            message: assistantInput.value,
            thread_id: tempThreadId.startsWith('temp_') ? null : tempThreadId
          });
        }

        assistantInput.value = '';
        uploadedFiles.value = [];
      };

      const newSelection = () => {
        selectedMessages.value = null;
        showSplash.value = true;
        selectedThread.value = null;
        selectedThreadTitle.value = '';
        titlesShown.value = false;
        uploadedFiles.value = [];
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
        isCalling.value = true;
        if (isRecording.value) {
          console.error("Recording is already in progress.");
          isCalling.value = false;
          return;
        }

        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          if (!stream.active) {
            console.error("The audio stream is not active. Please check microphone permissions and ensure it's not being used by another application.");
            return;
          }

          const options = { mimeType: 'audio/webm' };
          const mediaRecorder = new MediaRecorder(stream, options);

          mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) {
              console.log(`Received audio chunk of size: ${event.data.size}`);
              // Process the data only if the recorder is in the "recording" state
              if (mediaRecorder.state === "recording") {
                const reader = new FileReader();
                reader.onloadend = () => {
                  const base64data = reader.result;
                  console.log("Sending audio chunk to server");
                  socket.emit('audio_data', { data: base64data });
                };
                reader.readAsDataURL(event.data);
              } else {
                console.log(`Discarding chunk because the recorder state is: ${mediaRecorder.state}`);
              }
            }
          };

          mediaRecorder.onstart = () => {
            console.log("MediaRecorder started");
            isRecording.value = true;
          };

          mediaRecorder.onstop = () => {
            console.log("MediaRecorder stopped");
            isRecording.value = false;
          };

          // Start recording with a timeslice to ensure data is available at regular intervals
          mediaRecorder.start(1000);

          audioRecorder.value = mediaRecorder;
        } catch (error) {
          console.error("Error in starting MediaRecorder:", error);
        }
      };
  
      const stopRecording = () => {
        console.log("Stop recording button clicked");
        isCalling.value = false;
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
        titlesShown.value = false;
        const thread = threads.value.find(t => t.thread_id === thread_id);
        selectedThreadTitle.value = thread.title;
        console.log(selectedThreadTitle.value);

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

      const triggerFileExplorer = () => {
        if (fileInput.value) {
          fileInput.value.click();
        } else {
          console.error("File input not found");
        }
      };

      const handleFileSelection = (event) => {
        const files = event.target.files;
        if (!files.length) {
          console.log("No files selected.");
          return;
        }
        // Append the new files to the existing array instead of replacing it
        // const newFiles = Array.from(files).map(file => ({ name: file.name, size: file.size }));
        uploadedFiles.value = [...uploadedFiles.value, ...Array.from(files)];
      };

      const removeFile = (fileToRemove) => {
        uploadedFiles.value = uploadedFiles.value.filter(file => file !== fileToRemove);
      };

      const sendToInterpreter = () => {
        console.log("sent to interpreter");
      }

      const autoExpand = (event) => {
        const textarea = event.target;
          textarea.style.height = 'inherit';
        let maxHeight = 200; // Maximum height in pixels

        // Calculate the desired height
        let desiredHeight = Math.min(textarea.scrollHeight, maxHeight);

        textarea.style.height = `${desiredHeight}px`;
      };

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
        selectedThreadTitle,
        newSelection,
        loadTitlesOnly,
        titlesShown,
        isRecording,
        fileInput,
        triggerFileExplorer,
        handleFileSelection,
        sendToInterpreter,
        autoExpand,
        uploadedFiles,
        removeFile,
        showSplash,
        isCalling
      };
    }
  }
</script>
  
<style scoped>
#docs-sidebar {
  transition: transform 0.3s ease-in-out;
  transform: translateX(100%);
}

#docs-sidebar.off-canvas {
  transform: translateX(0);
}

#chatbox {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 100%;
  transition: left 0.3s ease-in-out;
}

body {
  overflow-x: hidden;
}

.selected-thread {
  background-color: #d1d5db;
}

.message p {
  white-space: pre-wrap;
}

.text-area {
  min-height: 40px;
  max-height: 200px;
  overflow-y: auto;
  width: 100%;
  resize: none;
  outline: none;
}

textarea:focus {
  outline: none !important;
  box-shadow: none !important;
}
</style>