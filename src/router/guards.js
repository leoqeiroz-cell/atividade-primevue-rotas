import { useAuthStore } from '../store/auth.js';

export function validateRouteAccess(to, auth = useAuthStore()) {
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return {
      name: 'login',
      query: { redirect: to.fullPath },
    };
  }

  if (to.meta.requiresRole && auth.user?.role !== to.meta.requiresRole) {
    return { name: 'home' };
  }

  return true;
}
