import { defineStore } from 'pinia';

const delay = (ms = 900) => new Promise((resolve) => setTimeout(resolve, ms));

const demoUsers = [
  {
    name: 'Cliente Prime',
    email: 'cliente@primeshop.com',
    password: '123456',
    role: 'CUSTOMER',
  },
  {
    name: 'Marina Admin',
    email: 'admin@primeshop.com',
    password: 'admin123',
    role: 'ADMIN',
  },
];

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    isLoading: false,
    registeredUsers: [],
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token && state.user),
  },
  actions: {
    async login(credentials) {
      this.isLoading = true;

      try {
        await delay();
        const normalizedEmail = credentials.email.trim().toLowerCase();
        const users = [...demoUsers, ...this.registeredUsers];
        const foundUser = users.find(
          (user) => user.email === normalizedEmail && user.password === credentials.password,
        );

        if (!foundUser) {
          throw new Error('Credenciais invalidas');
        }

        this.user = {
          name: foundUser.name,
          email: foundUser.email,
          role: foundUser.role,
        };
        this.token = `mock-token-${Date.now()}`;

        return this.user;
      } finally {
        this.isLoading = false;
      }
    },

    async register(account) {
      this.isLoading = true;

      try {
        await delay();
        const normalizedEmail = account.email.trim().toLowerCase();
        const users = [...demoUsers, ...this.registeredUsers];
        const emailAlreadyExists = users.some((user) => user.email === normalizedEmail);

        if (emailAlreadyExists) {
          throw new Error('Este e-mail ja esta cadastrado');
        }

        const newUser = {
          name: account.name.trim(),
          email: normalizedEmail,
          password: account.password,
          role: 'CUSTOMER',
        };

        this.registeredUsers.push(newUser);
        this.user = {
          name: newUser.name,
          email: newUser.email,
          role: newUser.role,
        };
        this.token = `mock-token-${Date.now()}`;

        return this.user;
      } finally {
        this.isLoading = false;
      }
    },

    logout() {
      this.user = null;
      this.token = null;
    },
  },
});
