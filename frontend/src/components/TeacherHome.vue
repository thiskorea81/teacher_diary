<template>
    <div>
      <h1>Teacher's Home</h1>
      <p>Welcome, {{ user.username }}! This is your dashboard.</p>
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  import { useMainStore } from '../stores/store.js';
  import { useRouter } from 'vue-router';
  
  export default {
    setup() {
      const store = useMainStore();
      const router = useRouter();
  
      const logout = () => {
        store.logout();
        router.push('/');
      };
  
      return {
        user: store.user,
        logout,
      };
    }
  }
  </script>
  