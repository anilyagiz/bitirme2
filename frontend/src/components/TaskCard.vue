<template>
  <div :class="cardClass" @click="$emit('click')">
    <div class="flex justify-between items-start mb-2">
      <h3 class="text-lg font-semibold">{{ assignment.location.name }}</h3>
      <span :class="statusClass">{{ statusText }}</span>
    </div>
    
    <div class="text-sm text-gray-600 mb-2">
      <p><strong>Bina:</strong> {{ assignment.location.building.name }}</p>
      <p v-if="assignment.location.department">
        <strong>Bölüm:</strong> {{ assignment.location.department.name }}
      </p>
      <p><strong>Periyot:</strong> {{ assignment.period.name }}</p>
    </div>
    
    <div v-if="assignment.staff_notes" class="text-sm bg-gray-100 p-2 rounded">
      <strong>Not:</strong> {{ assignment.staff_notes }}
    </div>
    
    <div v-if="assignment.supervisor_notes" class="text-sm bg-blue-100 p-2 rounded mt-2">
      <strong>Denetçi Notu:</strong> {{ assignment.supervisor_notes }}
    </div>
    
    <div v-if="assignment.rejection_reason" class="text-sm bg-red-100 p-2 rounded mt-2">
      <strong>Red Sebebi:</strong> {{ assignment.rejection_reason }}
    </div>
    
    <div v-if="assignment.rating" class="text-sm mt-2">
      <strong>Puan:</strong> {{ assignment.rating }}/5
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Assignment } from '../stores/tasks'

interface Props {
  assignment: Assignment
}

const props = defineProps<Props>()

const emit = defineEmits<{
  click: []
}>()

const cardClass = computed(() => {
  const baseClass = 'task-card cursor-pointer hover:shadow-lg transition-shadow'
  const statusClass = `task-card.${props.assignment.status}`
  return `${baseClass} ${statusClass}`
})

const statusClass = computed(() => {
  const baseClass = 'px-2 py-1 rounded text-sm font-semibold'
  const statusClasses = {
    pending: 'bg-gray-500 text-white',
    cleaned: 'bg-yellow-500 text-black',
    approved: 'bg-green-500 text-white',
    rejected: 'bg-red-500 text-white'
  }
  return `${baseClass} ${statusClasses[props.assignment.status]}`
})

const statusText = computed(() => {
  const statusMap = {
    pending: 'Beklemede',
    cleaned: 'Temizlendi',
    approved: 'Onaylandı',
    rejected: 'Reddedildi'
  }
  return statusMap[props.assignment.status]
})
</script>
