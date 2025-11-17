<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Atama Yönetimi</h1>
      <button
        @click="showCreateForm = true"
        class="large-button bg-blue-600 text-white hover:bg-blue-700"
      >
        + Yeni Atama
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      {{ error }}
    </div>

    <!-- Create Form -->
    <div v-if="showCreateForm" class="bg-white p-6 rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">Yeni Atama Oluştur</h2>
      <form @submit.prevent="handleCreate" class="space-y-4">
        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Periyot</label>
          <select
            v-model="newAssignment.period_id"
            required
            @focus="loadPeriods"
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Periyot Seçin</option>
            <option v-for="period in periods" :key="period.id" :value="period.id">
              {{ period.name }} ({{ period.status }})
            </option>
          </select>
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Mekan (Yaprak)</label>
          <select
            v-model="newAssignment.location_id"
            required
            @focus="loadLocations"
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Mekan Seçin</option>
            <option v-for="location in leafLocations" :key="location.id" :value="location.id">
              {{ location.name }} ({{ getLocationTypeName(location.location_type) }})
            </option>
          </select>
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Hizmetli (Staff)</label>
          <select
            v-model="newAssignment.staff_user_id"
            required
            @focus="loadUsers"
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Hizmetli Seçin</option>
            <option v-for="user in staffUsers" :key="user.id" :value="user.id">
              {{ user.full_name }} ({{ user.email }})
            </option>
          </select>
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Denetçi (Supervisor)</label>
          <select
            v-model="newAssignment.supervisor_user_id"
            required
            @focus="loadUsers"
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Denetçi Seçin</option>
            <option v-for="user in supervisorUsers" :key="user.id" :value="user.id">
              {{ user.full_name }} ({{ user.email }})
            </option>
          </select>
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

    <!-- Assignments List -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Mekan</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Hizmetli</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Denetçi</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Durum</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">İşlemler</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="loading && assignments.length === 0">
            <td colspan="5" class="px-6 py-4 text-center text-lg text-gray-500">
              Yükleniyor...
            </td>
          </tr>
          <tr v-else-if="assignments.length === 0">
            <td colspan="5" class="px-6 py-4 text-center text-lg text-gray-500">
              Henüz atama yok
            </td>
          </tr>
          <tr v-for="assignment in assignments" :key="assignment.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-lg text-gray-900">{{ assignment.location_id.substring(0, 8) }}...</td>
            <td class="px-6 py-4 text-lg text-gray-600">{{ assignment.staff_user_id.substring(0, 8) }}...</td>
            <td class="px-6 py-4 text-lg text-gray-600">{{ assignment.supervisor_user_id.substring(0, 8) }}...</td>
            <td class="px-6 py-4">
              <span class="inline-flex px-3 py-1 text-lg font-semibold rounded-full"
                :class="{
                  'bg-gray-100 text-gray-800': assignment.status === 'pending',
                  'bg-yellow-100 text-yellow-800': assignment.status === 'cleaned',
                  'bg-green-100 text-green-800': assignment.status === 'approved',
                  'bg-red-100 text-red-800': assignment.status === 'rejected'
                }"
              >
                {{ getStatusName(assignment.status) }}
              </span>
            </td>
            <td class="px-6 py-4">
              <button
                @click="handleDelete(assignment.id)"
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
import { ref, computed, onMounted } from 'vue'
import { useAssignmentStore } from '../../stores/assignments'
import { useLocationStore } from '../../stores/locations'
import { usePeriodStore } from '../../stores/periods'
import { useUserStore } from '../../stores/users'
import type { AssignmentCreate } from '../../stores/assignments'

const assignmentStore = useAssignmentStore()
const locationStore = useLocationStore()
const periodStore = usePeriodStore()
const userStore = useUserStore()

const { assignments, loading, error } = assignmentStore
const { locations } = locationStore
const { periods } = periodStore
const { users } = userStore

const showCreateForm = ref(false)
const newAssignment = ref<AssignmentCreate>({
  location_id: '',
  period_id: '',
  staff_user_id: '',
  supervisor_user_id: ''
})

const leafLocations = computed(() => {
  return locations.value.filter(l => l.is_leaf)
})

const staffUsers = computed(() => {
  return users.value.filter(u => u.role === 'staff')
})

const supervisorUsers = computed(() => {
  return users.value.filter(u => u.role === 'supervisor')
})

onMounted(() => {
  assignmentStore.fetchAssignments()
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

function getStatusName(status: string): string {
  const statusNames: Record<string, string> = {
    pending: 'Beklemede',
    cleaned: 'Temizlendi',
    approved: 'Onaylandı',
    rejected: 'Reddedildi'
  }
  return statusNames[status] || status
}

async function loadLocations() {
  if (locations.value.length === 0) {
    await locationStore.fetchLocations()
  }
}

async function loadPeriods() {
  if (periods.value.length === 0) {
    await periodStore.fetchPeriods()
  }
}

async function loadUsers() {
  if (users.value.length === 0) {
    await userStore.fetchUsers()
  }
}

async function handleCreate() {
  try {
    await assignmentStore.createAssignment(newAssignment.value)
    cancelCreate()
    await assignmentStore.fetchAssignments()
  } catch (err) {
    // Error is handled in store
  }
}

function cancelCreate() {
  showCreateForm.value = false
  newAssignment.value = {
    location_id: '',
    period_id: '',
    staff_user_id: '',
    supervisor_user_id: ''
  }
}

async function handleDelete(assignmentId: string) {
  if (confirm('Bu atamayı silmek istediğinizden emin misiniz?')) {
    try {
      await assignmentStore.deleteAssignment(assignmentId)
    } catch (err) {
      // Error is handled in store
    }
  }
}
</script>
