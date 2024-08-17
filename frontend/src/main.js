import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';

const app = createApp(App);

app.use(createPinia());  // Pinia 상태 관리 사용
app.use(router);         // Vue Router 사용

app.mount('#app');
