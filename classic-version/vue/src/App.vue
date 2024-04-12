<script setup lang="ts">
import { Toaster } from '@/components/ui/toast'
import { useColorMode } from '@vueuse/core'

useColorMode()
</script>

<template>
  <Toaster />
  <RouterView />
</template>
