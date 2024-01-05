export default {
  namespaced: true,
  state: {
    userId: localStorage.getItem('userId') === "null" ? null : localStorage.getItem('userId'),
    username: localStorage.getItem('username') === "null" ? null : localStorage.getItem('username'),
    access_csrf: localStorage.getItem('access_csrf') === "null" ? null : localStorage.getItem('access_csrf'),
    refresh_csrf: localStorage.getItem('refresh_csrf') === "null" ? null : localStorage.getItem('refresh_csrf'),
    isAuthenticated: localStorage.getItem('isAuthenticated') === "true" ? true : false,
    isGoogleLogin: localStorage.getItem('isGoogleLogin') === "true" ? true : false,
    googleUserCompleted: false
  }, 
  mutations: {
    setUserId(state, id) {
      if (id !== undefined) {
        state.userId = id;
        localStorage.setItem('userId', id);
      }
    },
    setUsername(state, user) {
      if (user !== undefined) {
        state.username = user;
        localStorage.setItem('username', user);
      }
    },
    setAccessCSRF(state, access_csrf) {
      if (access_csrf !== undefined) {
        state.access_csrf = access_csrf;
        localStorage.setItem('access_csrf', access_csrf);
      }
    },
    setRefreshCSRF(state, refresh_csrf) {
      if (refresh_csrf !== undefined) {
        state.refresh_csrf = refresh_csrf;
        localStorage.setItem('refresh_csrf', refresh_csrf);
      }
    },
    setAuthentication(state, status) {
      state.isAuthenticated = status;
      localStorage.setItem('isAuthenticated', status);
    },
    setGoogleLogin(state, status) {
      state.isGoogleLogin = status;
      localStorage.setItem('isGoogleLogin', status);
    },
    setGoogleUserDataCompleted(state, status) {
      state.googleUserDataCompleted = status;
    }
  },  
  actions: {
    setUserCredentials({ commit }, { id, username, access_csrf, refresh_csrf }) {
      commit('setUserId', id);
      commit('setUsername', username);
      commit('setAccessCSRF', access_csrf);
      commit('setRefreshCSRF', refresh_csrf);
      commit('setAuthentication', true);
    },
    logOut({commit}) {
      localStorage.removeItem('userId');
      localStorage.removeItem('username');
      localStorage.removeItem('access_csrf');
      localStorage.removeItem('refresh_csrf');
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('isGoogleLogin');

      commit('setUserId', null);
      commit('setUsername', null);
      commit('setAccessCSRF', null);
      commit('setRefreshCSRF', null);
      commit('setAuthentication', false);
      commit('setGoogleLogin', false);
    },
    updateCsrfTokens({ commit }, payload) {
      commit('setAccessCSRF', payload.access_csrf);
      commit('setRefreshCSRF', payload.refresh_csrf);
    },    
  },
  getters: {
    getUserId: state => state.userId,
    getUsername: state => state.username,
    getAccessCSRF: state => state.access_csrf,
    getRefreshCSRF: state => state.refresh_csrf,
    getAuthentication: state => state.isAuthenticated,
    getGoogleLogin: state => state.isGoogleLogin,
    googleUserDataCompleted: state => state.googleUserDataCompleted
  }
}