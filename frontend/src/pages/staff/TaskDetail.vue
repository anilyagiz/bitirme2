<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Görev Detayı</h1>
      <button
        @click="goBack"
        class="large-button bg-gray-600 text-white hover:bg-gray-700"
      >
        Geri Dön
      </button>
    </div>

    <div v-if="loading" class="text-center text-lg">
      Görev yükleniyor...
    </div>

    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      {{ error }}
    </div>

    <div v-else-if="task" class="space-y-6">
      <!-- Task Info -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4">{{ task.location.name }}</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-lg">
          <div>
            <strong>Bina:</strong> {{ task.location.building.name }}
          </div>
          <div v-if="task.location.department">
            <strong>Bölüm:</strong> {{ task.location.department.name }}
          </div>
          <div>
            <strong>Periyot:</strong> {{ task.period.name }}
          </div>
          <div>
            <strong>Durum:</strong> 
            <span :class="statusClass">{{ statusText }}</span>
          </div>
        </div>

        <div v-if="task.location.special_instructions" class="mt-4 p-3 bg-yellow-100 rounded">
          <strong>Özel Talimatlar:</strong> {{ task.location.special_instructions }}
        </div>
      </div>

      <!-- Staff Notes -->
      <div v-if="task.staff_notes" class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold mb-2">Notlarım</h3>
        <p>{{ task.staff_notes }}</p>
      </div>

      <!-- Supervisor Feedback -->
      <div v-if="task.supervisor_notes" class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold mb-2">Denetçi Notu</h3>
        <p>{{ task.supervisor_notes }}</p>
      </div>

      <div v-if="task.rejection_reason" class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold mb-2 text-red-600">Red Sebebi</h3>
        <p>{{ task.rejection_reason }}</p>
      </div>

      <div v-if="task.rating" class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold mb-2">Puan</h3>
        <p>{{ task.rating }}/5</p>
      </div>

      <!-- Clean Button -->
      <div v-if="canClean" class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold mb-4">Görev Tamamlama</h3>
        
        <div class="space-y-4">
          <TextInput
            id="notes"
            label="Not (Opsiyonel)"
            v-model="notes"
            placeholder="Temizlik hakkında notlarınızı yazın..."
          />
          
          <LargeButton
            @click="markAsCleaned"
            :disabled="loading || !navigator.onLine"
            variant="success"
            class="w-full"
          >
            {{ loading ? 'İşaretleniyor...' : 'TEMİZLEDİM' }}
          </LargeButton>
          
          <p v-if="!navigator.onLine" class="text-red-600 text-center">
            Bu işlem için internet bağlantısı gereklidir.
          </p>
        </div>
      </div>

      <!-- Status Info -->
      <div v-if="task.status === 'cleaned'" class="bg-yellow-100 p-4 rounded-lg">
        <p class="text-lg text-center">
          Görev tamamlandı. Denetçi onayını bekliyor.
        </p>
      </div>

      <div v-if="task.status === 'approved'" class="bg-green-100 p-4 rounded-lg">
        <p class="text-lg text-center text-green-800">
          Görev onaylandı! Tebrikler.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTaskStore } from '../../stores/tasks'
import TextInput from '../../components/ui/TextInput.vue'
import LargeButton from '../../components/ui/LargeButton.vue'

const route = useRoute()
const router = useRouter()
const taskStore = useTaskStore()

const taskId = route.params.id as string
const notes = ref('')
const online = ref(navigator.onLine)

const { loading, error, getTaskById, markAsCleaned } = taskStore

const task = computed(() => getTaskById(taskId))

const canClean = computed(() => 
  task.value && ['pending', 'rejected'].includes(task.value.status)
)

const statusClass = computed(() => {
  if (!task.value) return ''
  const classes = {
    pending: 'text-gray-600',
    cleaned: 'text-yellow-600',
    approved: 'text-green-600',
    rejected: 'text-red-600'
  }
  return classes[task.value.status]
})

const statusText = computed(() => {
  if (!task.value) return ''
  const texts = {
    pending: 'Beklemede',
    cleaned: 'Temizlendi',
    approved: 'Onaylandı',
    rejected: 'Reddedildi'
  }
  return texts[task.value.status]
})

const goBack = () => {
  router.push('/staff/tasks')
}

const handleMarkAsCleaned = async () => {
  try {
    await markAsCleaned(taskId, notes.value)
    notes.value = ''
    // Refresh task data
    await taskStore.fetchTasks()
  } catch (err) {
    // Error is handled by the store
  }
}

onMounted(() => {
  // Update online status
  const updateOnlineStatus = () => {
    online.value = navigator.onLine
  }
  
  window.addEventListener('online', updateOnlineStatus)
  window.addEventListener('offline', updateOnlineStatus)
})
</script>
