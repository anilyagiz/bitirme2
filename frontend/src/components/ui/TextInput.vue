<template>
  <div class="mb-4">
    <label v-if="label" :for="id" class="block text-lg font-semibold text-gray-700 mb-2">
      {{ label }}
    </label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :class="inputClass"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  id?: string
  label?: string
  type?: string
  modelValue?: string
  placeholder?: string
  disabled?: boolean
  error?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const inputClass = computed(() => {
  const baseClass = 'w-full px-4 py-3 text-lg border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
  const errorClass = props.error ? 'border-red-500' : 'border-gray-300'
  const disabledClass = props.disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'
  
  return `${baseClass} ${errorClass} ${disabledClass}`
})
</script>
