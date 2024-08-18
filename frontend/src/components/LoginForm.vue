<template>
  <div>
    <form @submit.prevent="login">
      <div>
        <label for="username">Username:</label>
        <input v-model="username" id="username" placeholder="Username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input v-model="password" id="password" type="password" placeholder="Password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    
    <p>
      회원이 아니십니까? <router-link to="/register">회원가입</router-link>
    </p>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useMainStore } from '../stores/store.js';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const store = useMainStore();
    const router = useRouter();

    const username = ref('');
    const password = ref('');

    const login = async () => {
      try {
        const response = await fetch('http://localhost:8000/token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({
            username: username.value,
            password: password.value
          })
        });

        const data = await response.json();

        if (response.ok) {
          store.login(data);

          // 로그인 성공 후 역할에 따라 페이지 리다이렉트
          if (data.role === 'admin') {
            router.push('/admin');  // 관리자 페이지로 리다이렉트
          } else if (data.role === 'teacher') {
            router.push('/teacher');  // 교사용 페이지로 리다이렉트
          } else if (data.role === 'student') {
            router.push('/student');  // 학생용 페이지로 리다이렉트
          } else if (data.role === 'parent') {
            router.push('/parent');  // 학부모용 페이지로 리다이렉트
          }
        } else {
          console.error('Login failed:', data);
        }
      } catch (error) {
        console.error('Error during login:', error);
      }
    };

    return { username, password, login };
  }
}
</script>
