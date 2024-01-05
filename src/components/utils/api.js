import axios from 'axios';
import { store } from '../../main';
import EventBus from './eventBus';

const instance = axios.create({
  baseURL: 'https://localhost:5000'
});

let isRefreshing = false;
let refreshSubscribers = [];

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

function refreshToken() {
  if (!isRefreshing) {
    isRefreshing = true;

    let csrf_refresh = store.getters['accounts/getRefreshCSRF']

    if (csrf_refresh) {
      return instance.post('/token_refresh', {}, {
        headers: {
          'X-CSRF-TOKEN': csrf_refresh
        },
        withCredentials: true
      })
      .then(response => {
        isRefreshing = false;
        store.dispatch('accounts/updateCsrfTokens', {
          access_csrf: response.data.csrf_tokens.access_csrf,
          refresh_csrf: response.data.csrf_tokens.refresh_csrf,
        });
        onRefreshed(response.data.access_token);
        return response.data.access_token;
      })
      .catch(error => {
        isRefreshing = false;
        EventBus.emit('token-refresh-failed');
        return Promise.reject(error);
      });
    } else if(store.getters['accounts/getGoogleLogin']) {
      return refreshGoogleAccessToken().then(token => {
        isRefreshing = false;
        onRefreshed(token);
        return token;
      })
      .catch(error => {
        isRefreshing = false;
        EventBus.emit('google-token-refresh-failed');
        return Promise.reject(error);
      });
    }
  }

  return new Promise(resolve => {
    subscribeTokenRefresh(token => {
      resolve(token);
    });
  });
}

instance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    // If error is 401 and it's not a retry attempt
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const token = await refreshToken();
        originalRequest.headers['Authorization'] = 'Bearer ' + token;

        // Check for admin status check request specifically
        if (originalRequest.url.includes('/admin_status_check')) {
          console.log('Retrying /admin_status_check after token refresh');
        } else {
          console.log('Retrying request to', originalRequest.url, 'after token refresh');
        }

        // Retry the original request with the new token
        return instance(originalRequest);
      } catch (refreshError) {
        console.error('Error during token refresh:', refreshError);
        return Promise.reject(refreshError);
      }
    }

    // For other types of errors, just pass it along
    return Promise.reject(error);
  }
);

export default instance;