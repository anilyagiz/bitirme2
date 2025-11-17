<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
      <button
        @click="fetchStats"
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
      İstatistikler yükleniyor...
    </div>

    <div v-else-if="stats" class="space-y-6">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow">
          <div class="text-center">
            <div class="text-3xl font-bold text-gray-600">{{ stats.pending }}</div>
            <div class="text-lg text-gray-500">Beklemede</div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow">
          <div class="text-center">
            <div class="text-3xl font-bold text-yellow-600">{{ stats.cleaned }}</div>
            <div class="text-lg text-gray-500">Temizlendi</div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow">
          <div class="text-center">
            <div class="text-3xl font-bold text-red-600">{{ stats.rejected }}</div>
            <div class="text-lg text-gray-500">Reddedildi</div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow">
          <div class="text-center">
            <div class="text-3xl font-bold text-green-600">{{ stats.approved }}</div>
            <div class="text-lg text-gray-500">Onaylandı</div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4">Hızlı İşlemler</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <router-link
            to="/admin/users"
            class="large-button bg-blue-600 text-white hover:bg-blue-700 text-center"
          >
            Kullanıcılar
          </router-link>
          
          <router-link
            to="/admin/buildings"
            class="large-button bg-green-600 text-white hover:bg-green-700 text-center"
          >
            Binalar
          </router-link>
          
          <router-link
            to="/admin/locations"
            class="large-button bg-purple-600 text-white hover:bg-purple-700 text-center"
          >
            Mekanlar
          </router-link>
          
          <router-link
            to="/admin/periods"
            class="large-button bg-yellow-600 text-white hover:bg-yellow-700 text-center"
          >
            Periyotlar
          </router-link>
          
          <router-link
            to="/admin/assignments"
            class="large-button bg-red-600 text-white hover:bg-red-700 text-center"
          >
            Atamalar
          </router-link>
          
          <router-link
            to="/admin/departments"
            class="large-button bg-indigo-600 text-white hover:bg-indigo-700 text-center"
          >
            Bölümler
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'

const adminStore = useAdminStore()

const { stats, loading, error, fetchDashboardStats } = adminStore

const fetchStats = fetchDashboardStats

onMounted(() => {
  fetchStats()
})
</script>
