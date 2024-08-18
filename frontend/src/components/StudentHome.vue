<template>
    <div>
      <h1>Student's Home</h1>
      <div>
        <p>{{ user.grade }} 학년 {{ user.classroom }} 반 {{ user.number }} 번 {{ user.username }}</p>
      </div>
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
        user: store.user,  // 스토어에서 사용자 정보를 가져옵니다.
        logout,
      };
    }
  }
  </script>
  
  <style>
  h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  h2 {
    font-size: 20px;
    margin-bottom: 10px;
  }
  
  p {
    font-size: 18px;
    margin: 5px 0;
  }
  
  button {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #42b983;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #38a172;
  }
  </style>
  