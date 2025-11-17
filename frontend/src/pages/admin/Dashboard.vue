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

    <!-- Quick Start Guide - Show when no stats or error -->
    <div v-if="!loading && (!stats || error)" class="space-y-6">
      <div class="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-lg">
        <h2 class="text-2xl font-bold text-blue-900 mb-4">🚀 Hoş Geldiniz!</h2>
        <p class="text-lg text-blue-800 mb-4">
          Sistemi kullanmaya başlamak için aşağıdaki adımları takip edin:
        </p>

        <div class="space-y-4">
          <div class="bg-white p-4 rounded-lg shadow-sm">
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                1
              </div>
              <div class="flex-1">
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Kullanıcıları Oluşturun</h3>
                <p class="text-lg text-gray-600 mb-3">Hizmetli (Staff) ve Denetçi (Supervisor) kullanıcıları ekleyin.</p>
                <router-link
                  to="/admin/users"
                  class="inline-block large-button bg-blue-600 text-white hover:bg-blue-700"
                >
                  Kullanıcı Ekle
                </router-link>
              </div>
            </div>
          </div>

          <div class="bg-white p-4 rounded-lg shadow-sm">
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-10 h-10 bg-green-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                2
              </div>
              <div class="flex-1">
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Binalar ve Bölümler Oluşturun</h3>
                <p class="text-lg text-gray-600 mb-3">Kampüsünüzdeki bina ve bölümleri tanımlayın.</p>
                <div class="flex gap-3">
                  <router-link
                    to="/admin/buildings"
                    class="inline-block large-button bg-green-600 text-white hover:bg-green-700"
                  >
                    Bina Ekle
                  </router-link>
                  <router-link
                    to="/admin/departments"
                    class="inline-block large-button bg-indigo-600 text-white hover:bg-indigo-700"
                  >
                    Bölüm Ekle
                  </router-link>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white p-4 rounded-lg shadow-sm">
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-10 h-10 bg-purple-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                3
              </div>
              <div class="flex-1">
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Mekanları Tanımlayın</h3>
                <p class="text-lg text-gray-600 mb-3">Temizlenecek mekanları (derslik, ofis, tuvalet vb.) ekleyin.</p>
                <router-link
                  to="/admin/locations"
                  class="inline-block large-button bg-purple-600 text-white hover:bg-purple-700"
                >
                  Mekan Ekle
                </router-link>
              </div>
            </div>
          </div>

          <div class="bg-white p-4 rounded-lg shadow-sm">
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-10 h-10 bg-yellow-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                4
              </div>
              <div class="flex-1">
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Periyot Oluşturun</h3>
                <p class="text-lg text-gray-600 mb-3">Temizlik dönemini (başlangıç-bitiş tarihi) tanımlayın ve aktif edin.</p>
                <router-link
                  to="/admin/periods"
                  class="inline-block large-button bg-yellow-600 text-white hover:bg-yellow-700"
                >
                  Periyot Ekle
                </router-link>
              </div>
            </div>
          </div>

          <div class="bg-white p-4 rounded-lg shadow-sm">
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-10 h-10 bg-red-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                5
              </div>
              <div class="flex-1">
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Atamaları Yapın</h3>
                <p class="text-lg text-gray-600 mb-3">Mekanları hizmetlilere ve denetçilere atayın.</p>
                <router-link
                  to="/admin/assignments"
                  class="inline-block large-button bg-red-600 text-white hover:bg-red-700"
                >
                  Atama Yap
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
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
