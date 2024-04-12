<script setup lang="ts">
import LoggedInLayout from '@/layouts/LoggedInLayout.vue'
</script>

<template>
  <LoggedInLayout class="main">
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
