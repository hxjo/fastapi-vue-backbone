<script setup lang="ts">
import ClientLayout from '@/layouts/ClientLayout.vue'
import RecoverPasswordForm from '@/forms/auth/RecoverPasswordForm.vue'
import { Link } from '@inertiajs/vue3'
import { Button } from '@/components/ui/button'
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
