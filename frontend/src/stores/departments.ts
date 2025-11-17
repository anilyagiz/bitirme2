import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from '../config/api'

export interface Department {
  id: string
  name: string
  code: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface DepartmentCreate {
  name: string
  code: string
  is_active?: boolean
}

export const useDepartmentStore = defineStore('departments', () => {
  const departments = ref<Department[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchDepartments(params: {
    page?: number
    page_size?: number
    search?: string
  } = {}): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await axios.get('/api/v1/departments', { params })
      departments.value = response.data.items
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Bölümler yüklenirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createDepartment(deptData: DepartmentCreate): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await axios.post('/api/v1/departments', deptData)
      departments.value.push(response.data)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Bölüm oluşturulurken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteDepartment(deptId: string): Promise<void> {
    loading.value = true
    error.value = null

    try {
      await axios.delete(`/api/v1/departments/${deptId}`)
      departments.value = departments.value.filter(d => d.id !== deptId)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Bölüm silinirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    departments,
    loading,
    error,
    fetchDepartments,
    createDepartment,
    deleteDepartment
  }
})
