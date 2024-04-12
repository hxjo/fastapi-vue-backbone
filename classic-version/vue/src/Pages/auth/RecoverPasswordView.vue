<script setup lang="ts">
import ClientLayout from '@/layouts/ClientLayout.vue'
import RecoverPasswordForm from '@/forms/auth/RecoverPasswordForm.vue'
import { Button } from '@/components/ui/button'
</script>

<template>
  <ClientLayout class="main">
    <template #header-top-right>
      <RouterLink to="/login">
        <Button variant="outline">
          {{ $t('auth.logIn.header') }}
        </Button>
      </RouterLink>
    </template>
    <RecoverPasswordForm />
  </ClientLayout>
</template>

<style scoped>
:deep(.main) {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
