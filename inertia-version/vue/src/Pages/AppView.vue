<script setup lang="ts">
import type { UserOut } from '@/api'
import LoggedInLayout from '@/layouts/LoggedInLayout.vue'

interface Props {
  user: UserOut
}
defineProps<Props>()
</script>

<template>
  <LoggedInLayout class="main" :user="user">
    <h1>Hello App (protected)</h1>
  </LoggedInLayout>
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
