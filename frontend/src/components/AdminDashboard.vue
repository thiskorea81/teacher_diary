<template>
    <div>
      <header>
        <h1>Admin Dashboard</h1>
        <button @click="logout">Logout</button>
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
          <span>
            {{ user.username }} ({{ user.role }}) - {{ user.email }}
            <span v-if="user.role === 'student' || user.role === 'parent'">
              | Grade: {{ user.grade }} | Classroom: {{ user.classroom }} | Number: {{ user.number }}
            </span>
          </span>
          <button @click="editUser(user)">Edit</button>
          <button @click="deleteUser(user.id)">Delete</button>
        </li>
      </ul>
  
      <div v-if="editingUser">
        <h2>Edit User</h2>
        <form @submit.prevent="updateUser">
          <div>
            <label for="editUsername">Username:</label>
            <input v-model="editingUser.username" id="editUsername" placeholder="Username" required />
          </div>
          <div>
            <label for="editEmail">Email:</label>
            <input v-model="editingUser.email" id="editEmail" type="email" placeholder="Email" required />
          </div>
          <div>
            <label for="editPassword">Password:</label>
            <input v-model="editingUser.password" id="editPassword" type="password" placeholder="Password" required />
          </div>
          <div>
            <label for="editRole">Role:</label>
            <select v-model="editingUser.role" id="editRole" required>
              <option value="student">Student</option>
              <option value="teacher">Teacher</option>
              <option value="parent">Parent</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div v-if="editingUser.role === 'student' || editingUser.role === 'parent'">
            <div>
              <label for="editGrade">Grade:</label>
              <input v-model="editingUser.grade" id="editGrade" type="number" placeholder="Grade" />
            </div>
            <div>
              <label for="editClassroom">Classroom:</label>
              <input v-model="editingUser.classroom" id="editClassroom" type="number" placeholder="Classroom" />
            </div>
            <div>
              <label for="editNumber">Number:</label>
              <input v-model="editingUser.number" id="editNumber" type="number" placeholder="Number" />
            </div>
          </div>
          <button type="submit">Update User</button>
        </form>
      </div>
  
      <!-- 데이터베이스 재설정 버튼 -->
      <div style="margin-top: 30px;">
        <button @click="resetDatabase" style="background-color: red; color: white;">
          Reset Database (Dangerous!)
        </button>
      </div>
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
      const email = ref('');
      const password = ref('');
      const users = ref([]);
      const editingUser = ref(null);
  
      const fetchUsers = async () => {
        const response = await fetch('http://localhost:8000/users');
        users.value = await response.json();
      };
  
      const addTeacher = async () => {
        await fetch('http://localhost:8000/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: username.value,
            email: email.value,
            password: password.value,
            role: 'teacher'
          })
        });
        fetchUsers();
      };
  
      const editUser = (user) => {
        editingUser.value = { ...user, password: '' };  // 패스워드는 초기화
      };
  
      const updateUser = async () => {
        await fetch(`http://localhost:8000/users/${editingUser.value.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(editingUser.value)
        });
        editingUser.value = null;
        fetchUsers();
      };
  
      const deleteUser = async (userId) => {
        await fetch(`http://localhost:8000/users/${userId}`, {
          method: 'DELETE'
        });
        fetchUsers();
      };
  
      const resetDatabase = async () => {
        if (confirm("Are you sure you want to reset the database? This action cannot be undone!")) {
          await fetch('http://localhost:8000/reset-database', {
            method: 'POST'
          });
          fetchUsers(); // 데이터베이스 재설정 후 사용자 목록 갱신
        }
      };
  
      const logout = () => {
        store.logout();
        router.push('/');
      };
  
      fetchUsers();
  
      return {
        username,
        email,
        password,
        users,
        editingUser,
        addTeacher,
        editUser,
        updateUser,
        deleteUser,
        resetDatabase,
        logout
      };
    }
  };
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
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  ul li {
    margin-bottom: 10px;
  }
  
  ul li span {
    margin-right: 10px;
  }
  
  ul li button {
    margin-left: 5px;
  }
  </style>
  