<template>
  <div v-if="!online" class="bg-red-600 text-white text-lg py-2 text-center">
    Çevrimdışı: İşlem yapabilmek için internete bağlanın.
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'

const online = ref(navigator.onLine)

const updateOnlineStatus = () => {
  online.value = navigator.onLine
}

onMounted(() => {
  window.addEventListener('online', updateOnlineStatus)
  window.addEventListener('offline', updateOnlineStatus)
})

onBeforeUnmount(() => {
  window.removeEventListener('online', updateOnlineStatus)
  window.removeEventListener('offline', updateOnlineStatus)
})
</script>
