import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from '../config/api'

export interface Period {
  id: string
  name: string
  start_date: string
  end_date: string
  status: 'planned' | 'active' | 'completed'
  created_at: string
  updated_at: string
}

export interface PeriodCreate {
  name: string
  start_date: string
  end_date: string
  status?: 'planned' | 'active' | 'completed'
}

export const usePeriodStore = defineStore('periods', () => {
  const periods = ref<Period[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchPeriods(params: {
    page?: number
    page_size?: number
    status?: string
  } = {}): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await axios.get('/api/v1/periods', { params })
      periods.value = response.data.items
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Periyotlar yüklenirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createPeriod(periodData: PeriodCreate): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await axios.post('/api/v1/periods', periodData)
      periods.value.push(response.data)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Periyot oluşturulurken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deletePeriod(periodId: string): Promise<void> {
    loading.value = true
    error.value = null

    try {
      await axios.delete(`/api/v1/periods/${periodId}`)
      periods.value = periods.value.filter(p => p.id !== periodId)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Periyot silinirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    periods,
    loading,
    error,
    fetchPeriods,
    createPeriod,
    deletePeriod
  }
})
