<script setup lang="ts">
import ClientLayout from '@/layouts/ClientLayout.vue'
import LoginForm from '@/forms/auth/LoginForm.vue'
import { Button } from '@/components/ui/button'
</script>

<template>
  <ClientLayout class="main">
    <template #header-top-right>
      <RouterLink to="/auth/signup">
        <Button variant="outline">
          {{ $t('auth.signUp.header') }}
        </Button>
      </RouterLink>
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
