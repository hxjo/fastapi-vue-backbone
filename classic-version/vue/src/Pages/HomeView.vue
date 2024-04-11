<script setup lang="ts">
import ClientLayout from '@/layouts/ClientLayout.vue'
import { Link } from '@inertiajs/vue3'
import type { UserOut } from '@/api'
import { Button } from '@/components/ui/button'

interface Props {
  user?: UserOut
}

defineProps<Props>()
</script>
<template>
  <ClientLayout class="main">
    <template #header-top-right>
      <Link v-if="user" href="/app">
        <Button variant="outline">
          {{ $t('goToApp') }}
        </Button>
      </Link>
      <Link v-else href="/login">
        <Button variant="outline">
          {{ $t('auth.logIn.header') }}
        </Button>
      </Link>
    </template>
    <h1>Hello World (unprotected)</h1>
  </ClientLayout>
</template>
<style scoped lang="postcss">
:deep(.main) {
  display: flex;
  justify-content: center;
  align-items: center;
}

h1 {
  font-size: 2rem;
}
</style>
