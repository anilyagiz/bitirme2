import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from '../config/api'

export interface User {
  id: string
  email: string
  full_name: string
  role: 'admin' | 'staff' | 'supervisor'
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  // Set up axios interceptor for auth
  axios.interceptors.request.use((config) => {
    if (token.value) {
      config.headers.Authorization = `Bearer ${token.value}`
    }
    return config
  })

  axios.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        logout()
      }
      return Promise.reject(error)
    }
  )

  async function login(credentials: LoginRequest): Promise<void> {
    loading.value = true
    try {
      const response = await axios.post<LoginResponse>('/api/v1/auth/login', credentials)
      const { access_token, user: userData } = response.data
      
      token.value = access_token
      user.value = userData
      localStorage.setItem('token', access_token)
    } catch (error) {
      throw error
    } finally {
      loading.value = false
    }
  }

  async function me(): Promise<void> {
    if (!token.value) return
    
    try {
      const response = await axios.get<User>('/api/v1/auth/me')
      user.value = response.data
    } catch (error) {
      logout()
      throw error
    }
  }

  function logout(): void {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  // Initialize user data if token exists
  if (token.value) {
    me()
  }

  return {
    token,
    user,
    loading,
    isAuthenticated,
    login,
    logout,
    me
  }
})
