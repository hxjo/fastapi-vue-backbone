<script setup lang="ts">
import { Toaster } from '@/components/ui/toast'
import { useColorMode } from '@vueuse/core'
import { useServerMessages } from '@/composables/useServerMessages'
useColorMode()
useServerMessages()
</script>

<template>
  <Toaster />
  <slot />
</template>

<style scoped lang="postcss"></style>
