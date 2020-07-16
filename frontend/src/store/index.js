import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    drawer: null,
    loggedIn: false,
    username: ''
  },
  getters: {
    loggedIn: state => state.loggedIn
  },
  mutations: {
    toggleDrawer(state) {
      state.drawer = !state.drawer
    },
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
