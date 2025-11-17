<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Mekan Yönetimi</h1>
      <button
        @click="showCreateForm = true"
        class="large-button bg-blue-600 text-white hover:bg-blue-700"
      >
        + Yeni Mekan
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      {{ error }}
    </div>

    <!-- Create Form -->
    <div v-if="showCreateForm" class="bg-white p-6 rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">Yeni Mekan Ekle</h2>
      <form @submit.prevent="handleCreate" class="space-y-4">
        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Mekan Adı</label>
          <input
            v-model="newLocation.name"
            type="text"
            required
            placeholder="Örn: A101 Derslik"
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Mekan Tipi</label>
          <select
            v-model="newLocation.location_type"
            required
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="derslik">Derslik</option>
            <option value="ofis">Ofis</option>
            <option value="tuvalet">Tuvalet</option>
            <option value="koridor">Koridor</option>
            <option value="diger">Diğer</option>
          </select>
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Bina</label>
          <select
            v-model="newLocation.building_id"
            required
            @focus="loadBuildings"
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Bina Seçin</option>
            <option v-for="building in buildings" :key="building.id" :value="building.id">
              {{ building.name }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Bölüm (Opsiyonel)</label>
          <select
            v-model="newLocation.department_id"
            @focus="loadDepartments"
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Bölüm Seçin (Opsiyonel)</option>
            <option v-for="dept in departments" :key="dept.id" :value="dept.id">
              {{ dept.name }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Kat Etiketi (Opsiyonel)</label>
          <input
            v-model="newLocation.floor_label"
            type="text"
            placeholder="Örn: 1. Kat"
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div class="flex items-center gap-3">
          <input
            v-model="newLocation.is_leaf"
            type="checkbox"
            id="is_leaf"
            class="w-6 h-6"
          />
          <label for="is_leaf" class="text-lg font-medium text-gray-700">
            Yaprak Mekan (Atama yapılabilir)
          </label>
        </div>

        <div class="flex gap-4">
          <button
            type="submit"
            :disabled="loading"
            class="large-button bg-green-600 text-white hover:bg-green-700"
          >
            {{ loading ? 'Kaydediliyor...' : 'Kaydet' }}
          </button>
          <button
            type="button"
            @click="cancelCreate"
            class="large-button bg-gray-600 text-white hover:bg-gray-700"
          >
            İptal
          </button>
        </div>
      </form>
    </div>

    <!-- Locations List -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Mekan Adı</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Tip</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Kat</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Yaprak</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Durum</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">İşlemler</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="loading && locations.length === 0">
            <td colspan="6" class="px-6 py-4 text-center text-lg text-gray-500">
              Yükleniyor...
            </td>
          </tr>
          <tr v-else-if="locations.length === 0">
            <td colspan="6" class="px-6 py-4 text-center text-lg text-gray-500">
              Henüz mekan yok
            </td>
          </tr>
          <tr v-for="location in locations" :key="location.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-lg text-gray-900">{{ location.name }}</td>
            <td class="px-6 py-4 text-lg text-gray-600">{{ getLocationTypeName(location.location_type) }}</td>
            <td class="px-6 py-4 text-lg text-gray-600">{{ location.floor_label || '-' }}</td>
            <td class="px-6 py-4">
              <span class="inline-flex px-3 py-1 text-lg font-semibold rounded-full"
                :class="location.is_leaf ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
              >
                {{ location.is_leaf ? 'Evet' : 'Hayır' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <span class="inline-flex px-3 py-1 text-lg font-semibold rounded-full"
                :class="location.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
              >
                {{ location.is_active ? 'Aktif' : 'Pasif' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <button
                @click="handleDelete(location.id)"
                :disabled="loading"
                class="text-red-600 hover:text-red-900 text-lg font-medium"
              >
                Sil
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useLocationStore } from '../../stores/locations'
import { useBuildingStore } from '../../stores/buildings'
import { useDepartmentStore } from '../../stores/departments'
import type { LocationCreate } from '../../stores/locations'

const locationStore = useLocationStore()
const buildingStore = useBuildingStore()
const deptStore = useDepartmentStore()

const { locations, loading, error } = locationStore
const { buildings } = buildingStore
const { departments } = deptStore

const showCreateForm = ref(false)
const newLocation = ref<LocationCreate>({
  name: '',
  location_type: 'derslik',
  building_id: '',
  department_id: undefined,
  is_leaf: true,
  floor_label: undefined,
  is_active: true
})

onMounted(() => {
  locationStore.fetchLocations()
})

function getLocationTypeName(type: string): string {
  const typeNames: Record<string, string> = {
    derslik: 'Derslik',
    ofis: 'Ofis',
    tuvalet: 'Tuvalet',
    koridor: 'Koridor',
    diger: 'Diğer'
  }
  return typeNames[type] || type
}

async function loadBuildings() {
  if (buildings.value.length === 0) {
    await buildingStore.fetchBuildings()
  }
}

async function loadDepartments() {
  if (departments.value.length === 0) {
    await deptStore.fetchDepartments()
  }
}

async function handleCreate() {
  try {
    await locationStore.createLocation(newLocation.value)
    cancelCreate()
    await locationStore.fetchLocations()
  } catch (err) {
    // Error is handled in store
  }
}

function cancelCreate() {
  showCreateForm.value = false
  newLocation.value = {
    name: '',
    location_type: 'derslik',
    building_id: '',
    department_id: undefined,
    is_leaf: true,
    floor_label: undefined,
    is_active: true
  }
}

async function handleDelete(locationId: string) {
  if (confirm('Bu mekanı silmek istediğinizden emin misiniz?')) {
    try {
      await locationStore.deleteLocation(locationId)
    } catch (err) {
      // Error is handled in store
    }
  }
}
</script>
