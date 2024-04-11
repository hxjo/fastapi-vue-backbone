<script setup lang="ts">
import ClientLayout from '@/layouts/ClientLayout.vue'
import { Link } from '@inertiajs/vue3'
import { Button } from '@/components/ui/button'
import { computed } from 'vue'
import type { MessageProps } from '@/messageProps'
import { useServerMessages } from '@/composables/useServerMessages'
import ResetPasswordForm from '@/forms/auth/ResetPasswordForm.vue'
interface Props extends MessageProps {
  email?: string
  token: string
}
const props = defineProps<Props>()

const message = computed(() => props.message)
useServerMessages(message)
</script>

<template>
  <ClientLayout class="main">
    <template #header-top-right>
      <Link href="/login">
        <Button variant="outline">
          {{ $t('auth.logIn.header') }}
        </Button>
      </Link>
    </template>
    <ResetPasswordForm v-if="email" :email="email" :token="token" />
    <h2 v-else>{{ $t('auth.errors.invalidToken') }}</h2>
  </ClientLayout>
</template>

<style scoped>
:deep(.main) {
  display: flex;
  justify-content: center;
  align-items: center;
}

h2 {
  font-size: 1.5rem;
  font-weight: 500;
}
</style>
