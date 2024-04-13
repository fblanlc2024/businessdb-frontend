import axios from 'axios';
import { store } from '../../main';
import EventBus from './eventBus';

const instance = axios.create({
  baseURL: `${process.env.VUE_APP_BACKEND_URL}`
});

let isRefreshing = false;
let refreshSubscribers = [];

// Components can subscribe so that they know when the token is being refreshed.
// This is especially useful in our ClientLookup page, where the admin status is crucial for the page to load entirely differently than for a regular user.
function subscribeTokenRefresh(cb) {
  refreshSubscribers.push(cb);
}

function onRefreshed(access_token) {
  refreshSubscribers.forEach(cb => cb(access_token));
  refreshSubscribers = [];
}

function refreshGoogleAccessToken() {
  return instance.post('/google_token_refresh', {}, {
    withCredentials: true
  })
  .then(response => {
    return response.data.access_token;
  })
  .catch(error => {
    EventBus.emit('google-token-refresh-failed');
    return Promise.reject(error);
  });
}

// Tries to hit the backend API endpoint to refresh the token.
// This method can retry up to twice before the router (another file) redirects them to the login page.
function refreshToken(retryCount = 0) {
  console.log("Starting token refresh process...");
  const maxRetries = 2;
  
  if (!isRefreshing) {
    isRefreshing = true;

    let csrf_refresh = store.getters['accounts/getRefreshCSRF'];

    const proceedWithRefresh = csrf_refresh ? instance.post('/token_refresh', {}, {
      headers: { 'X-CSRF-TOKEN': csrf_refresh },
      withCredentials: true
    }) : store.getters['accounts/getGoogleLogin'] ? refreshGoogleAccessToken() : Promise.reject(new Error("No valid refresh mechanism available."));

    return proceedWithRefresh.then(response => {
      isRefreshing = false;
      store.dispatch('accounts/updateCsrfTokens', {
        access_csrf: response.data.csrf_tokens.access_csrf,
        refresh_csrf: response.data.csrf_tokens.refresh_csrf,
      });
      console.log("Token refresh successful.");
      onRefreshed(response.data.access_token);
      return response.data.access_token;
    })
    .catch(error => {
      isRefreshing = false;
      console.log("Token refresh attempt failed with error:", error.toString());

      if (retryCount < maxRetries) {
        console.log(`Retrying token refresh (${retryCount + 1} of ${maxRetries} attempts)`);
        return refreshToken(retryCount + 1);
      } else {
        console.log("Maximum token refresh attempts reached. Emitting token-refresh-failed event.");
        EventBus.emit('token-refresh-failed');
        refreshSubscribers = [];
        return Promise.reject(error);
      }
    });
  } else {
    console.log("A token refresh is already in progress. Adding this request to the queue.");
    return new Promise((resolve, reject) => {
      subscribeTokenRefresh(token => {
        console.log("Token has been refreshed. Resuming queued request.");
        resolve(token);
      });

      EventBus.emit('token-refresh-failed', () => {
        console.log("Token refresh failed for a queued request.");
        reject(new Error("Token refresh failed."));
      });
    });
  }
}

// Before the specified methods/API endpoints, the Axios interceptor intercepts the requests and tries to fetch credentials via refreshing the token.
instance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const token = await refreshToken();
        originalRequest.headers['Authorization'] = 'Bearer ' + token;

        if (originalRequest.url.includes('/admin_status_check' || '/get-user-threads')) {
          console.log('Retrying /admin_status_check after token refresh');
        } else {
          console.log('Retrying request to', originalRequest.url, 'after token refresh');
        }
        return instance(originalRequest);
      } catch (refreshError) {
        console.error('Error during token refresh:', refreshError);
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default instance;