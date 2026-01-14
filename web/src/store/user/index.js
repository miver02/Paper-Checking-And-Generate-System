// src/store/user/index.js
import { defineStore } from 'pinia'
import state from './state'
import getters from './getters'
import authActions from './actions/auth'
import profileActions from './actions/profile'
import uiActions from './actions/ui'

export const useUserStore = defineStore('user', {
  state,
  getters,
  actions: {
    ...authActions,
    ...profileActions,
    ...uiActions,
  },
})
