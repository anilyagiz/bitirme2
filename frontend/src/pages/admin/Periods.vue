<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Periyot Yönetimi</h1>
      <button
        @click="showCreateForm = true"
        class="large-button bg-blue-600 text-white hover:bg-blue-700"
      >
        + Yeni Periyot
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      {{ error }}
    </div>

    <!-- Create Form -->
    <div v-if="showCreateForm" class="bg-white p-6 rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">Yeni Periyot Ekle</h2>
      <form @submit.prevent="handleCreate" class="space-y-4">
        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Periyot Adı</label>
          <input
            v-model="newPeriod.name"
            type="text"
            required
            placeholder="Örn: Ocak 2024"
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Başlangıç Tarihi</label>
          <input
            v-model="newPeriod.start_date"
            type="date"
            required
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Bitiş Tarihi</label>
          <input
            v-model="newPeriod.end_date"
            type="date"
            required
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Durum</label>
          <select
            v-model="newPeriod.status"
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="planned">Planlandı</option>
            <option value="active">Aktif</option>
            <option value="completed">Tamamlandı</option>
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

    <!-- Periods List -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Periyot Adı</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Başlangıç</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Bitiş</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Durum</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">İşlemler</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="loading && periods.length === 0">
            <td colspan="5" class="px-6 py-4 text-center text-lg text-gray-500">
              Yükleniyor...
            </td>
          </tr>
          <tr v-else-if="periods.length === 0">
            <td colspan="5" class="px-6 py-4 text-center text-lg text-gray-500">
              Henüz periyot yok
            </td>
          </tr>
          <tr v-for="period in periods" :key="period.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-lg text-gray-900">{{ period.name }}</td>
            <td class="px-6 py-4 text-lg text-gray-600">{{ formatDate(period.start_date) }}</td>
            <td class="px-6 py-4 text-lg text-gray-600">{{ formatDate(period.end_date) }}</td>
            <td class="px-6 py-4">
              <span class="inline-flex px-3 py-1 text-lg font-semibold rounded-full"
                :class="{
                  'bg-yellow-100 text-yellow-800': period.status === 'planned',
                  'bg-green-100 text-green-800': period.status === 'active',
                  'bg-gray-100 text-gray-800': period.status === 'completed'
                }"
              >
                {{ getStatusName(period.status) }}
              </span>
            </td>
            <td class="px-6 py-4">
              <button
                @click="handleDelete(period.id)"
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
import { usePeriodStore } from '../../stores/periods'
import type { PeriodCreate } from '../../stores/periods'

const periodStore = usePeriodStore()
const { periods, loading, error } = periodStore

const showCreateForm = ref(false)
const newPeriod = ref<PeriodCreate>({
  name: '',
  start_date: '',
  end_date: '',
  status: 'planned'
})

onMounted(() => {
  periodStore.fetchPeriods()
})

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('tr-TR')
}

function getStatusName(status: string): string {
  const statusNames: Record<string, string> = {
    planned: 'Planlandı',
    active: 'Aktif',
    completed: 'Tamamlandı'
  }
  return statusNames[status] || status
}

async function handleCreate() {
  try {
    await periodStore.createPeriod(newPeriod.value)
    cancelCreate()
    await periodStore.fetchPeriods()
  } catch (err) {
    // Error is handled in store
  }
}

function cancelCreate() {
  showCreateForm.value = false
  newPeriod.value = {
    name: '',
    start_date: '',
    end_date: '',
    status: 'planned'
  }
}

async function handleDelete(periodId: string) {
  if (confirm('Bu periyotu silmek istediğinizden emin misiniz?')) {
    try {
      await periodStore.deletePeriod(periodId)
    } catch (err) {
      // Error is handled in store
    }
  }
}
</script>
