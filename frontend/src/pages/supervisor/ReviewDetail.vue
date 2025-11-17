<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Görev İncelemesi</h1>
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

    <div v-else-if="review" class="space-y-6">
      <!-- Review Info -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4">{{ review.location.name }}</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-lg">
          <div>
            <strong>Bina:</strong> {{ review.location.building.name }}
          </div>
          <div v-if="review.location.department">
            <strong>Bölüm:</strong> {{ review.location.department.name }}
          </div>
          <div>
            <strong>Periyot:</strong> {{ review.period.name }}
          </div>
          <div>
            <strong>Hizmetli:</strong> {{ review.staff_user.full_name }}
          </div>
        </div>

        <div v-if="review.location.special_instructions" class="mt-4 p-3 bg-yellow-100 rounded">
          <strong>Özel Talimatlar:</strong> {{ review.location.special_instructions }}
        </div>

        <div v-if="review.staff_notes" class="mt-4 p-3 bg-blue-100 rounded">
          <strong>Hizmetli Notu:</strong> {{ review.staff_notes }}
        </div>
      </div>

      <!-- Approval Actions -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold mb-4">İnceleme</h3>
        
        <div class="space-y-4">
          <div>
            <label class="block text-lg font-semibold text-gray-700 mb-2">
              Puan (Opsiyonel)
            </label>
            <select
              v-model="rating"
              class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Puan seçin</option>
              <option value="1">1 - Çok Kötü</option>
              <option value="2">2 - Kötü</option>
              <option value="3">3 - Orta</option>
              <option value="4">4 - İyi</option>
              <option value="5">5 - Mükemmel</option>
            </select>
          </div>

          <TextInput
            id="notes"
            label="Not (Opsiyonel)"
            v-model="notes"
            placeholder="Tebrik notu veya önerilerinizi yazın..."
          />

          <div class="flex space-x-4">
            <LargeButton
              @click="approveReview"
              :disabled="loading"
              variant="success"
              class="flex-1"
            >
              {{ loading ? 'Onaylanıyor...' : 'ONAYLA' }}
            </LargeButton>
            
            <LargeButton
              @click="showRejectForm = true"
              :disabled="loading"
              variant="danger"
              class="flex-1"
            >
              REDDET
            </LargeButton>
          </div>
        </div>
      </div>

      <!-- Reject Form -->
      <div v-if="showRejectForm" class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold mb-4 text-red-600">Görev Reddi</h3>
        
        <div class="space-y-4">
          <TextInput
            id="rejectionReason"
            label="Red Sebebi (Zorunlu)"
            v-model="rejectionReason"
            placeholder="Red sebebini detaylı olarak açıklayın..."
            :error="rejectionError"
          />

          <div class="flex space-x-4">
            <LargeButton
              @click="rejectReview"
              :disabled="loading || !rejectionReason"
              variant="danger"
              class="flex-1"
            >
              {{ loading ? 'Reddediliyor...' : 'REDDET' }}
            </LargeButton>
            
            <LargeButton
              @click="showRejectForm = false"
              variant="secondary"
              class="flex-1"
            >
              İptal
            </LargeButton>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useReviewStore } from '../../stores/reviews'
import TextInput from '../../components/ui/TextInput.vue'
import LargeButton from '../../components/ui/LargeButton.vue'

const route = useRoute()
const router = useRouter()
const reviewStore = useReviewStore()

const reviewId = route.params.id as string
const rating = ref('')
const notes = ref('')
const rejectionReason = ref('')
const showRejectForm = ref(false)
const rejectionError = ref('')

const { loading, error, getReviewById, approveAssignment, rejectAssignment } = reviewStore

const review = computed(() => getReviewById(reviewId))

const goBack = () => {
  router.push('/supervisor/reviews')
}

const approveReview = async () => {
  try {
    await approveAssignment(
      reviewId,
      rating.value ? parseInt(rating.value) : undefined,
      notes.value || undefined
    )
    goBack()
  } catch (err) {
    // Error is handled by the store
  }
}

const rejectReview = async () => {
  if (!rejectionReason.value) {
    rejectionError.value = 'Red sebebi gereklidir'
    return
  }

  try {
    await rejectAssignment(reviewId, rejectionReason.value)
    goBack()
  } catch (err) {
    // Error is handled by the store
  }
}

onMounted(() => {
  // Component is ready
})
</script>
