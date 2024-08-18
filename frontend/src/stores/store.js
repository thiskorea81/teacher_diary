import { defineStore } from 'pinia';

export const useMainStore = defineStore('main', {
  state: () => ({
    user: null,
    isAuthenticated: false,
  }),
  actions: {
    login(userData) {
      this.user = {
        username: userData.username,
        email: userData.email,
        role: userData.role,
        grade: userData.grade,
        classroom: userData.classroom,
        number: userData.number,
      };
      this.isAuthenticated = true;
    },
    logout() {
      this.user = null;
      this.isAuthenticated = false;
    },
  },
});
