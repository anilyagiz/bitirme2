import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from '../config/api'
import type { Assignment, PaginatedResponse } from './tasks'

export const useReviewStore = defineStore('reviews', () => {
  const reviews = ref<Assignment[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchReviews(params: {
    page?: number
    page_size?: number
    status?: string
  } = {}): Promise<void> {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get<PaginatedResponse<Assignment>>('/api/v1/my/reviews', {
        params: {
          status: 'cleaned',
          ...params
        }
      })
      reviews.value = response.data.items
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'İncelemeler yüklenirken hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function approveAssignment(assignmentId: string, rating?: number, notes?: string): Promise<void> {
    loading.value = true
    error.value = null
    
    try {
      await axios.post(`/api/v1/my/reviews/${assignmentId}/approve`, {
        rating,
        supervisor_notes: notes
      })
      
      // Update local state
      const review = reviews.value.find(r => r.id === assignmentId)
      if (review) {
        review.status = 'approved'
        review.supervisor_reviewed_at = new Date().toISOString()
        if (rating) review.rating = rating
        if (notes) review.supervisor_notes = notes
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Onay işlemi sırasında hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function rejectAssignment(assignmentId: string, reason: string): Promise<void> {
    loading.value = true
    error.value = null
    
    try {
      await axios.post(`/api/v1/my/reviews/${assignmentId}/reject`, {
        rejection_reason: reason
      })
      
      // Update local state
      const review = reviews.value.find(r => r.id === assignmentId)
      if (review) {
        review.status = 'rejected'
        review.supervisor_reviewed_at = new Date().toISOString()
        review.rejection_reason = reason
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Red işlemi sırasında hata oluştu'
      throw err
    } finally {
      loading.value = false
    }
  }

  function getReviewById(id: string): Assignment | undefined {
    return reviews.value.find(review => review.id === id)
  }

  return {
    reviews,
    loading,
    error,
    fetchReviews,
    approveAssignment,
    rejectAssignment,
    getReviewById
  }
})
