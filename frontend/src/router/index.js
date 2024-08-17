import { createRouter, createWebHistory } from 'vue-router';
import LoginForm from '@/components/LoginForm.vue';
import RegisterForm from '@/components/RegisterForm.vue';
import UserHome from '@/components/UserHome.vue';
import AdminDashboard from '@/components/AdminDashboard.vue';
import { useMainStore } from '../stores/store.js';

const routes = [
  { path: '/', component: LoginForm },
  { path: '/register', component: RegisterForm },
  { path: '/home', component: UserHome },
  { 
    path: '/admin', 
    component: AdminDashboard,
    meta: { requiresAdmin: true }  // 관리자 권한 필요
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard
router.beforeEach((to, from, next) => {
  const store = useMainStore();
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    // 관리자 페이지로 접근 시도할 때
    if (!store.isAuthenticated || store.user.role !== 'admin') {
      alert('관리자 권한이 필요합니다.');
      next('/');  // 로그인 페이지로 리다이렉트
    } else {
      next();  // 접근 허용
    }
  } else {
    next();  // 접근 허용
  }
});

export default router;
