import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from '../config/api'

export interface Assignment {
  id: string
  location_id: string
  period_id: string
  staff_user_id: string
  supervisor_user_id: string
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

export interface AssignmentCreate {
  location_id: string
  period_id: string
  staff_user_id: string
  supervisor_user_id: string
}

export const useAssignmentStore = defineStore('assignments', () => {
  const assignments = ref<Assignment[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchAssignments(params: {
    page?: number
    page_size?: number
    period_id?: string
    status?: string
    staff_user_id?: string
    supervisor_user_id?: string
  } = {}): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await axios.get('/api/v1/assignments', { params })
      assignments.value = response.data.items
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Atamalar yüklenirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createAssignment(assignmentData: AssignmentCreate): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await axios.post('/api/v1/assignments', assignmentData)
      assignments.value.push(response.data)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Atama oluşturulurken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteAssignment(assignmentId: string): Promise<void> {
    loading.value = true
    error.value = null

    try {
      await axios.delete(`/api/v1/assignments/${assignmentId}`)
      assignments.value = assignments.value.filter(a => a.id !== assignmentId)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Atama silinirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    assignments,
    loading,
    error,
    fetchAssignments,
    createAssignment,
    deleteAssignment
  }
})
