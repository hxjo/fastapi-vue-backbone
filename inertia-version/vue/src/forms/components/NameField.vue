<script setup lang="ts">
import { vAutoAnimate } from '@formkit/auto-animate/vue'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'

interface Props {
  isFieldDirty: (field: string) => boolean
  name: string
  autocomplete: 'family-name' | 'given-name' | 'username'
  label: string
}
defineProps<Props>()
</script>

<template>
  <FormField v-slot="{ componentField }" :name="name">
    <FormItem v-auto-animate v-bind="$attrs" class="form-item">
      <FormLabel v-if="isFieldDirty(name)">{{ label }}</FormLabel>
      <FormControl>
        <Input
          type="text"
          :autocomplete="autocomplete"
          :placeholder="label"
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
