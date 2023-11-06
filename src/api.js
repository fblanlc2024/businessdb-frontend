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
  const csrfRefreshGoogle = Cookies.get('csrf_refresh_token');
  if (!csrfRefreshGoogle) {
    console.error('Refresh CSRF token is missing.');
    EventBus.emit('token-refresh-failed');
    return Promise.reject('CSRF token missing');
  }

  return instance.post('/google_token_refresh', {}, {
    headers: {
      'X-CSRF-TOKEN': csrfRefreshGoogle
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

  // Try to get the CSRF token for the refresh token from the Vuex store
  let csrf_refresh = store.getters['accounts/getRefreshCSRF'];

  // If it's not in the Vuex store, try to get it from the cookies
  if (!csrf_refresh) {
    csrf_refresh = Cookies.get('csrf_refresh_token');
    var testName = Cookies.get('account_name');
    console.log("[Interceptor] CSRF refresh token fetched from cookies:", csrf_refresh);
    console.log("tested token for cookie retrieval", testName);
  }

  // If we still don't have the CSRF token, we can't proceed with the refresh
  if (!csrf_refresh) {
    console.error("[Interceptor] Refresh CSRF token is missing.");
    EventBus.emit('token-refresh-failed');
    return Promise.reject('Refresh CSRF token missing');
  }

  // Check if the CSRF token is for Google's refresh token
  if (csrf_refresh === Cookies.get('csrf_refresh_token')) {
    // Use the Google token refresh method
    return refreshGoogleAccessToken();
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
