<template>
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
  </template>
  
  <script>
  import { io } from "socket.io-client";
import { ref } from 'vue';
  
  export default {
    setup() {
      const userMessage = ref('');
      const socket = io('https://localhost:5000'); 
      const aiResponse = ref('');
      const audioChunks = ref([]);
      const mediaRecorder = ref(null);
      const audioRecorder = ref(null);
      const isRecording = ref(false);
      const audioPlayer = ref(null);
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
  
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