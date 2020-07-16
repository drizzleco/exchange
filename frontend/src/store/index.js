import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    loggedIn: false,
    username: ''
  },
  getters: {
    loggedIn: state => state.loggedIn
  },
  mutations: {
    setLoggedIn(state) {
      state.loggedIn = true
    },
    setLoggedOut(state) {
      state.loggedIn = false
    },
    setUsername(state, username) {
      state.username = username
    }
  },
})
