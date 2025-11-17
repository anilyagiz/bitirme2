import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from '../config/api'

export interface Building {
  id: string
  name: string
  code: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface BuildingCreate {
  name: string
  code: string
  is_active?: boolean
}

export const useBuildingStore = defineStore('buildings', () => {
  const buildings = ref<Building[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchBuildings(params: {
    page?: number
    page_size?: number
    search?: string
  } = {}): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await axios.get('/api/v1/buildings', { params })
      buildings.value = response.data.items
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Binalar yüklenirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createBuilding(buildingData: BuildingCreate): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await axios.post('/api/v1/buildings', buildingData)
      buildings.value.push(response.data)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Bina oluşturulurken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteBuilding(buildingId: string): Promise<void> {
    loading.value = true
    error.value = null

    try {
      await axios.delete(`/api/v1/buildings/${buildingId}`)
      buildings.value = buildings.value.filter(b => b.id !== buildingId)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Bina silinirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    buildings,
    loading,
    error,
    fetchBuildings,
    createBuilding,
    deleteBuilding
  }
})
