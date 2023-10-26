<template>
    <div>
      <h1>Update and delete your account here.</h1>
      <button @click="updateAndDelete('update')">Update</button>
      <button @click="updateAndDelete('delete')">Delete</button>

      <div v-show="showUpdate">
        <input v-model="newUsername" placeholder="New Username" />
        <button @click="updateAccount">Confirm Update</button>
      </div>

      <div v-show="showDelete">
        Are you sure you want to delete your account?
        <button @click="deleteAccount">Confirm Delete</button>
      </div>
    </div>
</template>

<script>
import { ref, computed } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
    name: 'ManageAccount',
    setup() {
      var store = useStore();
      var router = useRouter();
      var showUpdate = ref(false);
      var showDelete = ref(false);
      var newUsername = ref('');

      var userId = computed(() => store.getters['accounts/getUserId']);
      var username = computed(() => store.getters['accounts/getUsername']);

      var updateAndDelete = (action) => {
        if(action == 'update') {
            showUpdate.value = true;
            showDelete.value = false;
        } else {
            showUpdate.value = false;
            showDelete.value = true;
        }
      }

      var redirectToLogin = () => {
        router.push({
          name: 'LoginPage'
        });
      }

      var updateAccount = () => {
        axios.put('https://localhost:5000/account', {
            username: username.value,  // Original username
            new_username: newUsername.value,
        },
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
          }
        })
        .then(response => {
            console.log(response.data);
            store.commit('accounts/setUsername', newUsername.value);
            redirectToLogin();
        })
        .catch(err => {
            if (err.response) {
                // Server responded with a status other than in the 2xx range
                console.error('Error updating account:', err.response.data);
            } else {
                console.error('Error:', err.message);
            }
        });
    }

    var deleteAccount = () => {
        axios.delete('https://localhost:5000/account', {
            data: { username: username.value } // Axios uses 'data' for DELETE requests
        },
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
          }
        })
        .then(response => {
            console.log(response.data);
            redirectToLogin();
        })
        .catch(err => {
            console.error('Error deleting account:', err);
        });
    }

      return {
        userId,
        username,
        newUsername,
        showUpdate,
        showDelete,
        updateAndDelete,
        updateAccount,
        deleteAccount,
        redirectToLogin
      };
    }
};
</script>