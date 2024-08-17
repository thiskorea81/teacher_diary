<template>
  <div>
    <h1>Welcome, {{ user.username }}</h1>
    <p>Email: {{ user.email }}</p>
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
      router.push('/');  // 로그아웃 후 로그인 화면으로 이동
    };

    return {
      user: store.user,
      logout,
    };
  }
}
</script>
