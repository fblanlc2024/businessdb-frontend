import { store } from '../../main';
import api from './api';

export async function checkAdminStatus() {
  try {
    const response = await api.get(`${process.env.VUE_APP_BACKEND_URL}/admin_status_check`, { withCredentials: true });
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
  // Waits for credentials to be fully fetched from Vue Store.
  await waitForDataCompletion();

  try {
    const response = await api.get(`${process.env.VUE_APP_BACKEND_URL}/admin_status_check`, { withCredentials: true });
    return response.data.isAdmin;
  } catch (error) {
    console.error('Error on retrying admin status check:', error);
    return false;
  }
}

// Watch property to update or unwatch as soon as the credentials are obtained or null
function waitForDataCompletion() {
  return new Promise((resolve) => {
    if (store.getters['googleUserCompleted']) {
      resolve();
    } else {
      const unwatch = store.watch(
        (state) => state.googleUserCompleted,
        (value) => {
          if (value) {
            unwatch();
            resolve();
          }
        }
      );
    }
  });
}
