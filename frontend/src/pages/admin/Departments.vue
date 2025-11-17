<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Bölüm Yönetimi</h1>
      <button
        @click="showCreateForm = true"
        class="large-button bg-blue-600 text-white hover:bg-blue-700"
      >
        + Yeni Bölüm
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      {{ error }}
    </div>

    <!-- Create Form -->
    <div v-if="showCreateForm" class="bg-white p-6 rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">Yeni Bölüm Ekle</h2>
      <form @submit.prevent="handleCreate" class="space-y-4">
        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Bölüm Adı</label>
          <input
            v-model="newDepartment.name"
            type="text"
            required
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Bölüm Kodu</label>
          <input
            v-model="newDepartment.code"
            type="text"
            required
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
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

    <!-- Departments List -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Bölüm Adı</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Kod</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Durum</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">İşlemler</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="loading && departments.length === 0">
            <td colspan="4" class="px-6 py-4 text-center text-lg text-gray-500">
              Yükleniyor...
            </td>
          </tr>
          <tr v-else-if="departments.length === 0">
            <td colspan="4" class="px-6 py-4 text-center text-lg text-gray-500">
              Henüz bölüm yok
            </td>
          </tr>
          <tr v-for="dept in departments" :key="dept.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-lg text-gray-900">{{ dept.name }}</td>
            <td class="px-6 py-4 text-lg text-gray-600">{{ dept.code }}</td>
            <td class="px-6 py-4">
              <span class="inline-flex px-3 py-1 text-lg font-semibold rounded-full"
                :class="dept.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
              >
                {{ dept.is_active ? 'Aktif' : 'Pasif' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <button
                @click="handleDelete(dept.id)"
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
import { useDepartmentStore } from '../../stores/departments'
import type { DepartmentCreate } from '../../stores/departments'

const deptStore = useDepartmentStore()
const { departments, loading, error } = deptStore

const showCreateForm = ref(false)
const newDepartment = ref<DepartmentCreate>({
  name: '',
  code: '',
  is_active: true
})

onMounted(() => {
  deptStore.fetchDepartments()
})

async function handleCreate() {
  try {
    await deptStore.createDepartment(newDepartment.value)
    cancelCreate()
    await deptStore.fetchDepartments()
  } catch (err) {
    // Error is handled in store
  }
}

function cancelCreate() {
  showCreateForm.value = false
  newDepartment.value = {
    name: '',
    code: '',
    is_active: true
  }
}

async function handleDelete(deptId: string) {
  if (confirm('Bu bölümü silmek istediğinizden emin misiniz?')) {
    try {
      await deptStore.deleteDepartment(deptId)
    } catch (err) {
      // Error is handled in store
    }
  }
}
</script>
