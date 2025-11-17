<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-bold text-gray-900">
          Temizlik Takip Sistemi
        </h2>
        <p class="mt-2 text-center text-lg text-gray-600">
          Hesabınıza giriş yapın
        </p>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="space-y-4">
          <TextInput
            id="email"
            label="E-posta"
            type="email"
            v-model="form.email"
            placeholder="ornek@email.com"
            :error="errors.email"
            required
          />
          
          <TextInput
            id="password"
            label="Şifre"
            type="password"
            v-model="form.password"
            placeholder="Şifrenizi girin"
            :error="errors.password"
            required
          />
        </div>

        <div v-if="error" class="text-red-600 text-center text-lg">
          {{ error }}
        </div>

        <LargeButton
          type="submit"
          :disabled="loading"
          class="w-full"
        >
          {{ loading ? 'Giriş yapılıyor...' : 'Giriş Yap' }}
        </LargeButton>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import TextInput from '../components/ui/TextInput.vue'
import LargeButton from '../components/ui/LargeButton.vue'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: ''
})

const errors = reactive({
  email: '',
  password: ''
})

const error = ref('')
const loading = ref(false)

const validateForm = () => {
  errors.email = ''
  errors.password = ''
  
  if (!form.email) {
    errors.email = 'E-posta gereklidir'
    return false
  }
  
  if (!form.password) {
    errors.password = 'Şifre gereklidir'
    return false
  }
  
  return true
}

const handleLogin = async () => {
  if (!validateForm()) return
  
  loading.value = true
  error.value = ''
  
  try {
    await authStore.login(form)
    
    // Redirect based on user role
    if (authStore.user?.role === 'admin') {
      router.push('/admin/dashboard')
    } else if (authStore.user?.role === 'staff') {
      router.push('/staff/tasks')
    } else if (authStore.user?.role === 'supervisor') {
      router.push('/supervisor/reviews')
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Giriş yapılırken hata oluştu'
  } finally {
    loading.value = false
  }
}
</script>
