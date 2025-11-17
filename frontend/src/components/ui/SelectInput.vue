<template>
  <div class="mb-4">
    <label v-if="label" :for="id" class="block text-lg font-semibold text-gray-700 mb-2">
      {{ label }}
    </label>
    <select
      :id="id"
      :value="modelValue"
      :disabled="disabled"
      :class="selectClass"
      @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
    >
      <option value="" disabled>{{ placeholder }}</option>
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Option {
  value: string
  label: string
}

interface Props {
  id?: string
  label?: string
  modelValue?: string
  placeholder?: string
  options: Option[]
  disabled?: boolean
  error?: string
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const selectClass = computed(() => {
  const baseClass = 'w-full px-4 py-3 text-lg border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
  const errorClass = props.error ? 'border-red-500' : 'border-gray-300'
  const disabledClass = props.disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'
  
  return `${baseClass} ${errorClass} ${disabledClass}`
})
</script>
