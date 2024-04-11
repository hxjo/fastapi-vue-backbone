<script setup lang="ts">
import { vAutoAnimate } from '@formkit/auto-animate/vue'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'

interface Props {
  isFieldDirty: (field: string) => boolean
}
defineProps<Props>()
</script>

<template>
  <FormField v-slot="{ componentField }" name="email">
    <FormItem v-auto-animate v-bind="$attrs" class="form-item">
      <FormLabel v-if="isFieldDirty('email')">{{ $t('auth.email') }}</FormLabel>
      <FormControl>
        <Input
          type="email"
          autocomplete="email"
          placeholder="name@example.com"
          v-bind="componentField"
        />
      </FormControl>
      <FormMessage />
    </FormItem>
  </FormField>
</template>

<style scoped>
.form-item {
  width: 100%;
}
</style>
