import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from '../config/api'

export interface Location {
  id: string
  name: string
  location_type: 'derslik' | 'ofis' | 'tuvalet' | 'koridor' | 'diger'
  location_subtype?: string
  building_id: string
  department_id?: string
  parent_location_id?: string
  is_leaf: boolean
  floor_label?: string
  area_sqm?: number
  special_instructions?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LocationCreate {
  name: string
  location_type: 'derslik' | 'ofis' | 'tuvalet' | 'koridor' | 'diger'
  location_subtype?: string
  building_id: string
  department_id?: string
  parent_location_id?: string
  is_leaf?: boolean
  floor_label?: string
  area_sqm?: number
  special_instructions?: string
  is_active?: boolean
}

export const useLocationStore = defineStore('locations', () => {
  const locations = ref<Location[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchLocations(params: {
    page?: number
    page_size?: number
    building_id?: string
    department_id?: string
    is_leaf?: boolean
    location_type?: string
    search?: string
  } = {}): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await axios.get('/api/v1/locations', { params })
      locations.value = response.data.items
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Mekanlar yüklenirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createLocation(locationData: LocationCreate): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await axios.post('/api/v1/locations', locationData)
      locations.value.push(response.data)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Mekan oluşturulurken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteLocation(locationId: string): Promise<void> {
    loading.value = true
    error.value = null

    try {
      await axios.delete(`/api/v1/locations/${locationId}`)
      locations.value = locations.value.filter(l => l.id !== locationId)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Mekan silinirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    locations,
    loading,
    error,
    fetchLocations,
    createLocation,
    deleteLocation
  }
})
