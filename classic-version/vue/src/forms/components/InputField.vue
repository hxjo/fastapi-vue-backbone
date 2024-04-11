<script setup lang="ts">
import { vAutoAnimate } from '@formkit/auto-animate/vue'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'

interface Props {
  isFieldDirty: (field: string) => boolean
  label: string
  fieldName: string
}
defineProps<Props>()
</script>

<template>
  <FormField :name="fieldName" v-slot="{ handleChange, handleBlur }">
    <FormItem v-auto-animate v-bind="$attrs" class="form-item">
      <FormLabel v-if="isFieldDirty(fieldName)">{{ label }}</FormLabel>
      <FormControl>
        <Input type="file" @blur="handleBlur" @change="handleChange" />
      </FormControl>
      <FormMessage />
    </FormItem>
  </FormField>
</template>

<style scoped lang="postcss">
.form-item {
  width: 100%;

  input {
    cursor: pointer;
  }
}
</style>
