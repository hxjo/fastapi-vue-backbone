<script setup lang="ts">
import ClientLayout from '@/layouts/ClientLayout.vue'
import LoginForm from '@/forms/auth/LoginForm.vue'
import { Link } from '@inertiajs/vue3'
import { Button } from '@/components/ui/button'
import { computed } from 'vue'
import type { MessageProps } from '@/messageProps'
import { useServerMessages } from '@/composables/useServerMessages'
interface Props extends MessageProps {}
const props = defineProps<Props>()

const message = computed(() => props.message)
useServerMessages(message)
</script>

<template>
  <ClientLayout class="main">
    <template #header-top-right>
      <Link href="/signup">
        <Button variant="outline">
          {{ $t('auth.signUp.header') }}
        </Button>
      </Link>
    </template>
    <LoginForm />
  </ClientLayout>
</template>

<style scoped>
:deep(.main) {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
