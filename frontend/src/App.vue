<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <ConnectivityBanner />
    <AppHeader v-if="isAuthenticated" />
    <main class="container mx-auto px-4 py-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from './stores/auth'
import AppHeader from './components/AppHeader.vue'
import ConnectivityBanner from './components/ConnectivityBanner.vue'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>
