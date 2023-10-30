import axios from 'axios';
import Cookies from 'js-cookie';
import EventBus from './eventBus';
import { store } from './main';

// Create an Axios instance
const instance = axios.create({
  baseURL: 'https://localhost:5000'
});

// Method to refresh the Google access token
function refreshGoogleAccessToken() {
  const csrfRefresh = Cookies.get('csrf_refresh_token');
  if (!csrfRefresh) {
    console.error('Refresh CSRF token is missing.');
    EventBus.emit('token-refresh-failed');
    return Promise.reject('CSRF token missing');
  }

  return instance.post('/google_token_refresh', {}, {
    headers: {
      'X-CSRF-TOKEN': csrfRefresh
    },
    withCredentials: true
  })
  .then(response => {
    console.log('Token refreshed successfully:', response.data);
    // Update CSRF tokens in the Vuex store if needed
    store.dispatch('accounts/updateCsrfTokens', {
      access_csrf: response.data.csrf_tokens.access_csrf,
      refresh_csrf: response.data.csrf_tokens.refresh_csrf
    });
    return response.data;
  })
  .catch(error => {
    console.error('Error refreshing Google token:', error);
    EventBus.emit('token-refresh-failed');
    return Promise.reject(error);
  });
}

// Function to request a token refresh
function refreshToken() {
  console.log("[Interceptor] Attempting to refresh token...");

  // Get the CSRF token for the refresh token from your Vuex store or wherever you've stored it
  const csrf_refresh = store.getters['accounts/getRefreshCSRF'];
  console.log("LOOK AT THIS CSRF REFRESH", csrf_refresh);

  // Check if the CSRF token is for Google's refresh token
  if (csrf_refresh === Cookies.get('refresh_csrf_cookie')) {
    return refreshGoogleAccessToken(); // Use the Google token refresh method
  } else {
    // Handle non-Google token refresh here
    return instance.post('/token_refresh', {}, {
      headers: {
        'X-CSRF-TOKEN': csrf_refresh
      },
      withCredentials: true
    })
    .then(response => {
      console.log("[Interceptor] Token refreshed successfully:", response.data);
      return response.data;
    })
    .catch(err => {
      console.error("[Interceptor] Error refreshing token:", err);
      EventBus.emit('token-refresh-failed');
      throw err;  // Propagate the error
    });
  }
}

instance.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    const originalRequest = error.config;

    // If response is a 401, and this isn't a retry request, and the request is NOT for token_refresh, retry it
    if (error.response.status === 401 && 
        !originalRequest._retry && 
        originalRequest.url !== '/token_refresh' &&
        originalRequest.url !== '/google_token_refresh') { // Add check for Google token refresh endpoint
      originalRequest._retry = true;  // mark the request as a retry

      return refreshToken().then(() => {
        return instance(originalRequest);
      });
    }

    // If the error is from the /token_refresh or /google_token_refresh endpoint and it's a 401
    if (error.response.status === 401 && 
        (originalRequest.url === '/token_refresh' || originalRequest.url === '/google_token_refresh')) {
      EventBus.emit('token-refresh-failed');
      return Promise.reject(error);
    }

    // If error is something other than 401, or it's a retry request that failed, reject
    return Promise.reject(error);
  }
);

export default instance;
