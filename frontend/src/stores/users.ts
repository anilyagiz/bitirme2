import { defineStore } from 'pinia'
import { ref } from 'vue'
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

export interface UserCreate {
  email: string
  full_name: string
  role: 'admin' | 'staff' | 'supervisor'
  password: string
  is_active?: boolean
}

export const useUserStore = defineStore('users', () => {
  const users = ref<User[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchUsers(params: {
    page?: number
    page_size?: number
    role?: string
    search?: string
  } = {}): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await axios.get('/api/v1/users', { params })
      users.value = response.data.items
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Kullanıcılar yüklenirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createUser(userData: UserCreate): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await axios.post('/api/v1/users', userData)
      users.value.push(response.data)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Kullanıcı oluşturulurken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteUser(userId: string): Promise<void> {
    loading.value = true
    error.value = null

    try {
      await axios.delete(`/api/v1/users/${userId}`)
      users.value = users.value.filter(u => u.id !== userId)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Kullanıcı silinirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    users,
    loading,
    error,
    fetchUsers,
    createUser,
    deleteUser
  }
})
