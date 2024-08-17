<template>
  <form @submit.prevent="register">
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
    <div>
      <label for="role">Role:</label>
      <select v-model="role" id="role" required>
        <option value="student">Student</option>
        <option value="parent">Parent</option>
      </select>
    </div>
    <button type="submit">Register</button>
  </form>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      role: 'student'  // 기본 값은 'student'
    }
  },
  methods: {
    async register() {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: this.username,
          email: this.email,
          password: this.password,
          role: this.role
        })
      });
      const data = await response.json();
      console.log(data);
    }
  }
}
</script>
