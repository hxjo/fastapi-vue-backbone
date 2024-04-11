<script setup lang="ts">
import ThemeSelector from '@/components/site-settings/SiteSettings.vue'
import { Link, usePage } from '@inertiajs/vue3'
import { computed } from 'vue'

const page = usePage()
const href = computed(() => {
  return new URL(page.url).pathname
})
</script>

<template>
  <header>
    <div class="logo-and-settings">
      <Link v-if="href !== '/'" href="/" class="logo"> Acme Inc. </Link>
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
