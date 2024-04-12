<script setup lang="ts">
import ThemeSelector from '@/components/site-settings/SiteSettings.vue'
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<template>
  <header>
    <div class="logo-and-settings">
      <RouterLink v-if="route.path !== '/'" to="/" class="logo"> Acme Inc. </RouterLink>
      <span v-else class="logo">Acme Inc.</span>
      <ThemeSelector />
    </div>
    <slot name="top-right" />
  </header>
</template>

<style scoped lang="postcss">
header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--header-height);
  padding: 0 20px;
  border-bottom-width: 1px;
  .logo-and-settings {
    display: flex;
    gap: 8px;
    align-items: center;
    .logo {
      color: var(--primary);
      text-transform: uppercase;
      font-weight: 700;
    }
  }
}
</style>
