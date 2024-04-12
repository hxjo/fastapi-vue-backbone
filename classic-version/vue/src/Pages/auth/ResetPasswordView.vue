<script setup lang="ts">
import ClientLayout from '@/layouts/ClientLayout.vue'
import { Button } from '@/components/ui/button'
import ResetPasswordForm from '@/forms/auth/ResetPasswordForm.vue'
import { OpenAPI, type UserOut, UsersService } from '@/api'
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue'

const route = useRoute()
const token = route.query.token as string
OpenAPI.TOKEN = token
const user = ref<UserOut | null>()

onMounted(async () => {
  user.value = await UsersService.getUserMeApiV1UsersMeGet()
})
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
    <ResetPasswordForm v-if="user?.email" :email="user.email" :token="token" />
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
