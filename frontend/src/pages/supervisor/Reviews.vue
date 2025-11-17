<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Onay Bekleyen Görevler</h1>
      <button
        @click="fetchReviews"
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
      İncelemeler yükleniyor...
    </div>

    <div v-else-if="reviews.length === 0" class="text-center text-lg text-gray-600">
      Onay bekleyen görev bulunmuyor.
    </div>

    <div v-else class="grid gap-4">
      <div v-for="review in reviews" :key="review.id">
        <TaskCard :assignment="review" @click="goToReviewDetail(review.id)" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useReviewStore } from '../../stores/reviews'
import TaskCard from '../../components/TaskCard.vue'

const router = useRouter()
const reviewStore = useReviewStore()

const { reviews, loading, error, fetchReviews } = reviewStore

const goToReviewDetail = (reviewId: string) => {
  router.push(`/supervisor/reviews/${reviewId}`)
}

onMounted(() => {
  fetchReviews()
})
</script>
