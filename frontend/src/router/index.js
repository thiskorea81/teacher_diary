import { createRouter, createWebHistory } from 'vue-router';
import LoginForm from '@/components/LoginForm.vue';
import RegisterForm from '@/components/RegisterForm.vue';
import AdminDashboard from '@/components/AdminDashboard.vue';
import TeacherHome from '@/components/TeacherHome.vue';
import StudentHome from '@/components/StudentHome.vue';
import ParentHome from '@/components/ParentHome.vue';
import { useMainStore } from '../stores/store.js';

const routes = [
  { path: '/', component: LoginForm },
  { path: '/register', component: RegisterForm },
  { path: '/admin', component: AdminDashboard, meta: { requiresAdmin: true } },  // 관리자 페이지
  { path: '/teacher', component: TeacherHome, meta: { requiresAuth: true } },  // 교사용 페이지
  { path: '/student', component: StudentHome, meta: { requiresAuth: true } },  // 학생용 페이지
  { path: '/parent', component: ParentHome, meta: { requiresAuth: true } },  // 학부모용 페이지
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard
router.beforeEach((to, from, next) => {
  const store = useMainStore();

  // 페이지 접근 권한 확인
  if (to.matched.some(record => record.meta.requiresAuth || record.meta.requiresAdmin)) {
    if (!store.isAuthenticated) {
      next('/');  // 인증되지 않은 사용자는 로그인 페이지로 리다이렉트
    } else if (to.meta.requiresAdmin && store.user.role !== 'admin') {
      next('/');  // 관리자가 아닌 경우 접근 차단
    } else if (to.path === '/teacher' && store.user.role !== 'teacher') {
      next('/');  // 교사가 아닌 경우 접근 차단
    } else if (to.path === '/student' && store.user.role !== 'student') {
      next('/');  // 학생이 아닌 경우 접근 차단
    } else if (to.path === '/parent' && store.user.role !== 'parent') {
      next('/');  // 학부모가 아닌 경우 접근 차단
    } else {
      next();  // 접근 허용
    }
  } else {
    next();  // 접근 허용
  }
});

export default router;
