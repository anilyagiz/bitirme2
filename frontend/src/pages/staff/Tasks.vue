<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Görevlerim</h1>
      <button
        @click="fetchTasks"
        class="large-button bg-blue-600 text-white hover:bg-blue-700"
        :disabled="loading"
      >
        {{ loading ? 'Yükleniyor...' : 'Yenile' }}
      </button>
    </div>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      {{ error }}
    </div>

    <div v-if="loading" class="text-center text-lg">
      Görevler yükleniyor...
    </div>

    <div v-else-if="tasks.length === 0" class="text-center text-lg text-gray-600">
      Henüz görev atanmamış.
    </div>

    <div v-else class="grid gap-4">
      <!-- Rejected tasks first -->
      <div v-for="task in rejectedTasks" :key="task.id">
        <TaskCard :assignment="task" @click="goToTaskDetail(task.id)" />
      </div>
      
      <!-- Other tasks -->
      <div v-for="task in otherTasks" :key="task.id">
        <TaskCard :assignment="task" @click="goToTaskDetail(task.id)" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTaskStore } from '../../stores/tasks'
import TaskCard from '../../components/TaskCard.vue'

const router = useRouter()
const taskStore = useTaskStore()

const { tasks, loading, error, fetchTasks } = taskStore

const rejectedTasks = computed(() => 
  tasks.filter(task => task.status === 'rejected')
)

const otherTasks = computed(() => 
  tasks.filter(task => task.status !== 'rejected')
)

const goToTaskDetail = (taskId: string) => {
  router.push(`/staff/tasks/${taskId}`)
}

onMounted(() => {
  fetchTasks()
})
</script>
