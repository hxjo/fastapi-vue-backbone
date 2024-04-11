<script setup lang="ts">
import { vAutoAnimate } from '@formkit/auto-animate/vue'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Button } from '@/components/ui/button'
import { Icon } from '@iconify/vue'
import { Input } from '@/components/ui/input'
import { ref } from 'vue'

interface Props {
  isFieldDirty: (field: string) => boolean
  name: 'password' | 'passwordConfirm'
}

defineProps<Props>()

const isPasswordVisible = ref(false)
</script>

<template>
  <FormField v-slot="{ componentField }" :name="name">
    <FormItem v-auto-animate v-bind="$attrs" class="form-item">
      <FormLabel v-if="isFieldDirty(name)">{{ $t(`auth.${name}`) }}</FormLabel>
      <FormMessage />
      <FormControl>
        <div class="password-field">
          <Input
            :type="isPasswordVisible ? 'text' : 'password'"
            autocomplete="new-password"
            :placeholder="$t(`auth.${name}`)"
            v-bind="componentField"
          />

          <Button variant="outline" type="button" @click="isPasswordVisible = !isPasswordVisible">
            <Icon :icon="isPasswordVisible ? `radix-icons:eye-open` : `radix-icons:eye-closed`" />
          </Button>
        </div>
      </FormControl>
    </FormItem>
  </FormField>
</template>

<style scoped lang="postcss">
.form-item {
  width: calc(100% - 60px);
}
.password-field {
  position: relative;
  button {
    position: absolute;
    top: 0;
    right: -60px;
  }
}
</style>
