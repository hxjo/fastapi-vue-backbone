<script setup lang="ts">
import ClientLayout from '@/layouts/ClientLayout.vue'
import { Button } from '@/components/ui/button'
import { useCurrentUserStore } from '@/stores/currentUser'
import { storeToRefs } from 'pinia'

const { isLoggedIn } = storeToRefs(useCurrentUserStore())
</script>
<template>
  <ClientLayout class="main">
    <template #header-top-right>
      <RouterLink v-if="isLoggedIn" to="/app">
        <Button variant="outline">
          {{ $t('goToApp') }}
        </Button>
      </RouterLink>
      <RouterLink v-else to="/auth/login">
        <Button variant="outline">
          {{ $t('auth.logIn.header') }}
        </Button>
      </RouterLink>
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
