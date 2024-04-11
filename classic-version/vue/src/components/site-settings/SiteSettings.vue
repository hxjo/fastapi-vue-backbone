<script setup lang="ts">
import { Icon } from '@iconify/vue'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
  DropdownMenuLabel,
  DropdownMenuSeparator
} from '@/components/ui/dropdown-menu'
import { Button } from '@/components/ui/button'
import ThemeSettingsSubmenu from '@/components/site-settings/ThemeSettingsSubmenu.vue'
import LangSettingsSubmenu from '@/components/site-settings/LangSettingsSubmenu.vue'
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="outline">
        <Icon icon="radix-icons:gear" />
        <span class="sr-only">Site settings</span>
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="start" :align-offset="-6" side="bottom" :side-offset="8">
      <DropdownMenuLabel>{{ $t('settings.header') }}</DropdownMenuLabel>
      <DropdownMenuSeparator />
      <ThemeSettingsSubmenu />
      <LangSettingsSubmenu />
    </DropdownMenuContent>
  </DropdownMenu>
</template>

<style scoped lang="postcss"></style>
