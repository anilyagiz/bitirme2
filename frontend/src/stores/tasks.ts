import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from '../config/api'

export interface Assignment {
  id: string
  location: {
    id: string
    name: string
    location_type: string
    location_subtype?: string
    building: {
      id: string
      name: string
    }
    department?: {
      id: string
      name: string
    }
    floor_label?: string
  }
  period: {
    id: string
    name: string
    status: string
  }
  staff_user: {
    id: string
    full_name: string
  }
  supervisor_user: {
    id: string
    full_name: string
  }
  status: 'pending' | 'cleaned' | 'approved' | 'rejected'
  staff_notes?: string
  supervisor_notes?: string
  rejection_reason?: string
  rating?: number
  staff_completed_at?: string
  supervisor_reviewed_at?: string
  created_at: string
  updated_at: string
}

export interface PaginatedResponse<T> {
  items: T[]
  page: number
  page_size: number
  total: number
}

export const useTaskStore = defineStore('tasks', () => {
  const tasks = ref<Assignment[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchTasks(params: {
    page?: number
    page_size?: number
    status?: string
    period_id?: string
  } = {}): Promise<void> {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get<PaginatedResponse<Assignment>>('/api/v1/my/assignments', {
        params
      })
      tasks.value = response.data.items
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Görevler yüklenirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function markAsCleaned(assignmentId: string, notes?: string): Promise<void> {
    loading.value = true
    error.value = null
    
    try {
      await axios.post(`/api/v1/my/assignments/${assignmentId}/clean`, {
        staff_notes: notes
      })
      
      // Update local state
      const task = tasks.value.find(t => t.id === assignmentId)
      if (task) {
        task.status = 'cleaned'
        task.staff_completed_at = new Date().toISOString()
        if (notes) {
          task.staff_notes = notes
        }
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Görev işaretlenirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  function getTaskById(id: string): Assignment | undefined {
    return tasks.value.find(task => task.id === id)
  }

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    markAsCleaned,
    getTaskById
  }
})
