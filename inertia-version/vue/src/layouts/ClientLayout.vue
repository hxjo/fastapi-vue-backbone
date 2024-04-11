<script setup lang="ts">
import ClientHeader from '@/components/ClientHeader.vue'
defineOptions({
  inheritAttrs: false
})
</script>

<template>
  <div>
    <ClientHeader>
      <template #top-right>
        <slot name="header-top-right" />
      </template>
    </ClientHeader>
    <main v-bind="$attrs">
      <slot />
    </main>
  </div>
</template>

<style scoped lang="postcss">
main {
  padding: 20px;
  min-height: calc(100dvh - var(--header-height));
}
</style>
