import axios from 'axios';
import Cookies from 'js-cookie';
import { store } from '../../main';
import EventBus from './eventBus';

const instance = axios.create({
  baseURL: 'https://localhost:5000'
});

let isRefreshing = false;
let refreshSubscribers = [];

// Put the requests in a stack to be pushed in a queue?
function subscribeTokenRefresh(cb) {
  refreshSubscribers.push(cb);
}

function onRefreshed(access_token) {
  refreshSubscribers.forEach(cb => cb(access_token));
  refreshSubscribers = [];
}

function refreshToken() {
  if (!isRefreshing) {
    isRefreshing = true;

    let csrf_refresh = store.getters['accounts/getRefreshCSRF'] || Cookies.get('csrf_refresh_token');

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
  }

  return new Promise(resolve => {
    subscribeTokenRefresh(token => {
      resolve(token);
    });
  });
}

instance.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    const originalRequest = error.config;

    if (error.response.status === 401 && originalRequest.url.includes('/admin_status_check')) {
      if (!originalRequest._retryAdmin) {
        originalRequest._retryAdmin = true;

        return refreshToken().then(token => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token;
          return instance(originalRequest);
        });
      }
    }

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      return refreshToken().then(token => {
        originalRequest.headers['Authorization'] = 'Bearer ' + token;
        return instance(originalRequest);
      });
    }

    return Promise.reject(error);
  }
);

export default instance;