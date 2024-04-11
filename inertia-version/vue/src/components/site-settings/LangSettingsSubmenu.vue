<script setup lang="ts">
import { Icon } from '@iconify/vue'
import {
  DropdownMenuItem,
  DropdownMenuSub,
  DropdownMenuSubTrigger,
  DropdownMenuSubContent,
  DropdownMenuPortal
} from '@/components/ui/dropdown-menu'
import { useI18n } from 'vue-i18n'
import { useCookies } from '@vueuse/integrations/useCookies'
const i18n = useI18n()
const cookies = useCookies()

function setLocale(locale: string) {
  i18n.locale.value = locale
  cookies.set('locale', locale)
}
</script>

<template>
  <DropdownMenuSub>
    <DropdownMenuSubTrigger class="dropdown-trigger">
      <Icon icon="radix-icons:globe" />
      {{ $t('settings.language.header') }}
      <span class="sr-only">Language settings</span>
    </DropdownMenuSubTrigger>
    <DropdownMenuPortal>
      <DropdownMenuSubContent side="right" :side-offset="8">
        <div class="item-list">
          <DropdownMenuItem @click="() => setLocale('fr')" class="menu-item">
            Français
          </DropdownMenuItem>
          <DropdownMenuItem @click="() => setLocale('en')" class="menu-item">
            English
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
