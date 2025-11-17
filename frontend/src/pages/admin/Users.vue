<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Kullanıcı Yönetimi</h1>
      <button
        @click="showCreateForm = true"
        class="large-button bg-blue-600 text-white hover:bg-blue-700"
      >
        + Yeni Kullanıcı
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      {{ error }}
    </div>

    <!-- Create Form -->
    <div v-if="showCreateForm" class="bg-white p-6 rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">Yeni Kullanıcı Ekle</h2>
      <form @submit.prevent="handleCreate" class="space-y-4">
        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">E-posta</label>
          <input
            v-model="newUser.email"
            type="email"
            required
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Ad Soyad</label>
          <input
            v-model="newUser.full_name"
            type="text"
            required
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Rol</label>
          <select
            v-model="newUser.role"
            required
            class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="admin">Admin</option>
            <option value="staff">Staff (Hizmetli)</option>
            <option value="supervisor">Supervisor (Denetçi)</option>
          </select>
        </div>

        <div>
          <label class="block text-lg font-medium text-gray-700 mb-2">Şifre</label>
          <input
            v-model="newUser.password"
            type="password"
            required
            minlength="8"
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

    <!-- Users List -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Ad Soyad</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">E-posta</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Rol</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">Durum</th>
            <th class="px-6 py-3 text-left text-lg font-semibold text-gray-900">İşlemler</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="loading && users.length === 0">
            <td colspan="5" class="px-6 py-4 text-center text-lg text-gray-500">
              Yükleniyor...
            </td>
          </tr>
          <tr v-else-if="users.length === 0">
            <td colspan="5" class="px-6 py-4 text-center text-lg text-gray-500">
              Henüz kullanıcı yok
            </td>
          </tr>
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-lg text-gray-900">{{ user.full_name }}</td>
            <td class="px-6 py-4 text-lg text-gray-600">{{ user.email }}</td>
            <td class="px-6 py-4">
              <span class="inline-flex px-3 py-1 text-lg font-semibold rounded-full"
                :class="{
                  'bg-red-100 text-red-800': user.role === 'admin',
                  'bg-blue-100 text-blue-800': user.role === 'staff',
                  'bg-green-100 text-green-800': user.role === 'supervisor'
                }"
              >
                {{ getRoleName(user.role) }}
              </span>
            </td>
            <td class="px-6 py-4">
              <span class="inline-flex px-3 py-1 text-lg font-semibold rounded-full"
                :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
              >
                {{ user.is_active ? 'Aktif' : 'Pasif' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <button
                @click="handleDelete(user.id)"
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
import { useUserStore } from '../../stores/users'
import type { UserCreate } from '../../stores/users'

const userStore = useUserStore()
const { users, loading, error } = userStore

const showCreateForm = ref(false)
const newUser = ref<UserCreate>({
  email: '',
  full_name: '',
  role: 'staff',
  password: '',
  is_active: true
})

onMounted(() => {
  userStore.fetchUsers()
})

function getRoleName(role: string): string {
  const roleNames: Record<string, string> = {
    admin: 'Admin',
    staff: 'Hizmetli',
    supervisor: 'Denetçi'
  }
  return roleNames[role] || role
}

async function handleCreate() {
  try {
    await userStore.createUser(newUser.value)
    cancelCreate()
    await userStore.fetchUsers()
  } catch (err) {
    // Error is handled in store
  }
}

function cancelCreate() {
  showCreateForm.value = false
  newUser.value = {
    email: '',
    full_name: '',
    role: 'staff',
    password: '',
    is_active: true
  }
}

async function handleDelete(userId: string) {
  if (confirm('Bu kullanıcıyı silmek istediğinizden emin misiniz?')) {
    try {
      await userStore.deleteUser(userId)
    } catch (err) {
      // Error is handled in store
    }
  }
}
</script>
