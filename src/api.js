import axios from 'axios';
import { store } from './main';

// Create an Axios instance
const instance = axios.create({
    baseURL: 'https://localhost:5000'
});

// Function to request a token refresh
function refreshToken() {
    console.log("[Interceptor] Attempting to refresh token...");

    // Get the CSRF token for the refresh token from your Vuex store or wherever you've stored it
    const csrf_refresh = store.getters['accounts/getRefreshCSRF'];
    console.log("LOOK AT THIS CSRF REFRESH", csrf_refresh);

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
        throw err;  // Propagate the error
    });
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
            originalRequest.url !== '/token_refresh') {
            originalRequest._retry = true;  // mark the request as a retry

            return refreshToken().then(() => {
                return instance(originalRequest);
            });
        }

        // If error is something other than 401, or it's a retry request that failed, or it's a failed token_refresh, reject
        return Promise.reject(error);
    }
);

export default instance;