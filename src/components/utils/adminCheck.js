import { store } from '../../main'; // Assuming store is accessible here
import api from './api';

export async function checkAdminStatus() {
  try {
    const response = await api.get('https://localhost:5000/admin_status_check', { withCredentials: true });
    return response.data.isAdmin;
  } catch (error) {
    console.error('Error checking admin status:', error);
    if (error.response && error.response.status === 401) {
      return await retryRequest();
    }
    return false;
  }
}

async function retryRequest() {
  // Wait for the user data or token refresh completion
  await waitForDataCompletion();

  // Retry the request
  try {
    const response = await api.get('https://localhost:5000/admin_status_check', { withCredentials: true });
    return response.data.isAdmin;
  } catch (error) {
    console.error('Error on retrying admin status check:', error);
    return false;
  }
}

function waitForDataCompletion() {
  return new Promise((resolve) => {
    // Check if the data retrieval is already completed
    if (store.getters['googleUserCompleted']) {
      resolve();
    } else {
      // Watch for the completion
      const unwatch = store.watch(
        (state) => state.googleUserCompleted,
        (value) => {
          if (value) {
            unwatch(); // Stop watching once the data is retrieved
            resolve();
          }
        }
      );
    }
  });
}
