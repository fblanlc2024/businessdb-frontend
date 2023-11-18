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
  return instance.post('/google_token_refresh', {}, {
    withCredentials: true
  })
  .then(response => {
    console.log('Token refreshed successfully:', response.data);
    // Update the stored Google access token
    localStorage.setItem('google_access_token', response.data.access_token);
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

  // Try to get the CSRF token for the refresh token from the Vuex store
  let csrf_refresh = store.getters['accounts/getRefreshCSRF'];

  // If it's not in the Vuex store, try to get it from the cookies
  if (!csrf_refresh) {
    csrf_refresh = Cookies.get('csrf_refresh_token');
    var testName = Cookies.get('account_name');
    console.log("[Interceptor] CSRF refresh token fetched from cookies:", csrf_refresh);
    console.log("tested token for cookie retrieval", testName);
  }

  // If CSRF token is found, use it to refresh the token
  if (csrf_refresh) {
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
  } else {
    // If CSRF token is not found, proceed with Google token refresh
    console.log("[Interceptor] CSRF token not found, refreshing Google token...");
    return refreshGoogleAccessToken()
    .then(response => {
      console.log("[Interceptor] Google token refreshed successfully:", response.data);
      return response.data;
    })
    .catch(error => {
      console.error('Error refreshing Google token:', error);
      EventBus.emit('token-refresh-failed');
      return Promise.reject(error);
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
