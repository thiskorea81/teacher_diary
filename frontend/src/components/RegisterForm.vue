<template>
  <div>
    <h1>Register</h1>
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
        <select v-model="role" id="role" @change="onRoleChange" required>
          <option value="student">Student</option>
          <option value="parent">Parent</option>
        </select>
      </div>
      <div v-if="role === 'student' || role === 'parent'">
        <div>
          <label for="grade">Grade:</label>
          <input v-model="grade" id="grade" type="number" placeholder="Grade" required />
        </div>
        <div>
          <label for="classroom">Classroom:</label>
          <input v-model="classroom" id="classroom" type="number" placeholder="Classroom" required />
        </div>
        <div>
          <label for="number">Number:</label>
          <input v-model="number" id="number" type="number" placeholder="Number" required />
        </div>
      </div>
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const username = ref('');
    const email = ref('');
    const password = ref('');
    const role = ref('student');
    const grade = ref(null);
    const classroom = ref(null);
    const number = ref(null);
    const router = useRouter();

    const onRoleChange = () => {
      grade.value = null;
      classroom.value = null;
      number.value = null;
    };

    const register = async () => {
      try {
        const response = await fetch('http://localhost:8000/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: username.value,
            email: email.value,
            password: password.value,
            role: role.value,
            grade: grade.value,
            classroom: classroom.value,
            number: number.value
          })
        });

        if (response.ok) {
          console.log('Registration successful');
          router.push('/');
        } else {
          const data = await response.json();
          console.error('Registration failed:', data);
        }
      } catch (error) {
        console.error('Error during registration:', error);
      }
    };

    return {
      username,
      email,
      password,
      role,
      grade,
      classroom,
      number,
      register,
      onRoleChange,
    };
  }
}
</script>
