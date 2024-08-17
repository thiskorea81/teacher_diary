<template>
    <div>
      <header>
        <h1>Admin Dashboard</h1>
        <button @click="logout">Logout</button> <!-- 로그아웃 버튼 추가 -->
      </header>
      
      <h2>Add New Teacher</h2>
      <form @submit.prevent="addTeacher">
        <div>
          <label for="username">Username:</label>
          <input v-model="username" id="username" placeholder="Username" required />
        </div>
        <div>
          <label for="email">Email:</label>
          <input v-model="email" id="email" type="email" placeholder="Email" required />
        </div>
        <div>
          <label for="password">Password:</label>
          <input v-model="password" id="password" type="password" placeholder="Password" required />
        </div>
        <button type="submit">Add Teacher</button>
      </form>
  
      <h2>All Users</h2>
      <ul>
        <li v-for="user in users" :key="user.id">
          {{ user.username }} ({{ user.role }}) - {{ user.email }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { useMainStore } from '../stores/store.js';
  import { useRouter } from 'vue-router';
  
  export default {
    setup() {
      const store = useMainStore();
      const router = useRouter();
  
      const username = ref('');
      const email = ref('');
      const password = ref('');
      const users = ref([]);
  
      const addTeacher = async () => {
        const response = await fetch('http://localhost:8000/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: username.value,
            email: email.value,
            password: password.value,
            role: 'teacher'  // 강제로 'teacher' 역할을 부여
          })
        });
        const data = await response.json();
        console.log(data);
        fetchUsers();  // 사용자를 다시 로드하여 업데이트
      };
  
      const fetchUsers = async () => {
        const response = await fetch('http://localhost:8000/users', {
          method: 'GET',
        });
        const data = await response.json();
        users.value = data;
      };
  
      const logout = () => {
        store.logout();
        router.push('/');  // 로그아웃 후 로그인 화면으로 이동
      };
  
      onMounted(() => {
        fetchUsers();  // 컴포넌트가 마운트될 때 사용자 목록을 불러옵니다.
      });
  
      return {
        username,
        email,
        password,
        users,
        addTeacher,
        logout,
      };
    }
  }
  </script>
  
  <style>
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #f8f9fa;
    padding: 10px;
    border-bottom: 1px solid #ddd;
  }
  
  header h1 {
    margin: 0;
  }
  
  header button {
    background-color: #dc3545;
    color: white;
    border: none;
    padding: 8px 16px;
    cursor: pointer;
    font-size: 16px;
    border-radius: 4px;
  }
  
  header button:hover {
    background-color: #c82333;
  }
  </style>
  