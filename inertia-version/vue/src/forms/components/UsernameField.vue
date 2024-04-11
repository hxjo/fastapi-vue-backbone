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
  <FormField v-slot="{ componentField }" name="username">
    <FormItem v-auto-animate v-bind="$attrs" class="form-item">
      <FormLabel v-if="isFieldDirty('username')">{{ $t('user.username') }}</FormLabel>
      <FormControl>
        <Input
          type="text"
          autocomplete="username"
          :placeholder="$t('user.username')"
          v-bind="componentField"
        />
      </FormControl>
      <FormMessage />
    </FormItem>
  </FormField>
</template>

<style scoped lang="postcss">
.form-item {
  width: 100%;
}
</style>
