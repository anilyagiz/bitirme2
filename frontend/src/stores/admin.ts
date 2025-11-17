import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from '../config/api'

export interface DashboardStats {
  period_id: string
  pending: number
  cleaned: number
  rejected: number
  approved: number
}

export const useAdminStore = defineStore('admin', () => {
  const stats = ref<DashboardStats | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchDashboardStats(): Promise<void> {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get<DashboardStats>('/api/v1/dashboard/active-period-stats')
      stats.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'İstatistikler yüklenirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    stats,
    loading,
    error,
    fetchDashboardStats
  }
})
