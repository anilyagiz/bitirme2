<template>
  <header class="bg-white shadow-sm border-b">
    <div class="container mx-auto px-4 py-4">
      <div class="flex justify-between items-center">
        <h1 class="text-xl font-bold text-gray-800">Temizlik Takip Sistemi</h1>
        
        <nav class="flex space-x-4">
          <router-link
            v-if="user?.role === 'admin'"
            to="/admin/dashboard"
            class="text-lg text-gray-600 hover:text-blue-600"
          >
            Dashboard
          </router-link>
          <router-link
            v-if="user?.role === 'staff'"
            to="/staff/tasks"
            class="text-lg text-gray-600 hover:text-blue-600"
          >
            Görevlerim
          </router-link>
          <router-link
            v-if="user?.role === 'supervisor'"
            to="/supervisor/reviews"
            class="text-lg text-gray-600 hover:text-blue-600"
          >
            İncelemeler
          </router-link>
          
          <div class="flex items-center space-x-4">
            <span class="text-lg text-gray-700">{{ user?.full_name }}</span>
            <button
              @click="logout"
              class="text-lg text-red-600 hover:text-red-800"
            >
              Çıkış
            </button>
          </div>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const user = authStore.user

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
