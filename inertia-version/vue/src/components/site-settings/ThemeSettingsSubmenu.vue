<script setup lang="ts">
import { useColorMode } from '@vueuse/core'
import { Icon } from '@iconify/vue'
import {
  DropdownMenuItem,
  DropdownMenuSub,
  DropdownMenuSubTrigger,
  DropdownMenuSubContent,
  DropdownMenuPortal
} from '@/components/ui/dropdown-menu'

const mode = useColorMode()
</script>

<template>
  <DropdownMenuSub>
    <DropdownMenuSubTrigger class="dropdown-trigger">
      <Icon v-if="mode === 'light'" icon="radix-icons:sun" />
      <Icon v-if="mode === 'dark'" icon="radix-icons:moon" />
      {{ $t('settings.theme.header') }}
      <span class="sr-only">Theme settings</span>
    </DropdownMenuSubTrigger>
    <DropdownMenuPortal>
      <DropdownMenuSubContent side="right" :side-offset="8">
        <div class="item-list">
          <DropdownMenuItem @click="mode = 'light'" class="menu-item">
            <Icon icon="radix-icons:sun" />
            {{ $t('settings.theme.light') }}
          </DropdownMenuItem>
          <DropdownMenuItem @click="mode = 'dark'" class="menu-item">
            <Icon icon="radix-icons:moon" />
            {{ $t('settings.theme.dark') }}
          </DropdownMenuItem>
          <DropdownMenuItem @click="mode = 'auto'" class="menu-item">
            <Icon icon="radix-icons:lightning-bolt" />
            {{ $t('settings.theme.auto') }}
          </DropdownMenuItem>
        </div>
      </DropdownMenuSubContent>
    </DropdownMenuPortal>
  </DropdownMenuSub>
</template>

<style scoped lang="postcss">
.menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dropdown-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
