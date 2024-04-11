<script setup lang="ts">
import type { UserOut } from '@/api'
import type { MessageProps } from '@/messageProps'
import { computed } from 'vue'
import { useServerMessages } from '@/composables/useServerMessages'
import LoggedInLayout from '@/layouts/LoggedInLayout.vue'

interface Props extends MessageProps {
  user: UserOut
}
const props = defineProps<Props>()

const message = computed(() => props.message)
useServerMessages(message)
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
