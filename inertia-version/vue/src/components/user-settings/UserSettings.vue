<script setup lang="ts">
import { Icon } from '@iconify/vue'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuItem
} from '@/components/ui/dropdown-menu'
import type { UserOut } from '@/api'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { computed } from 'vue'
import { Link } from '@inertiajs/vue3'
import { DialogTrigger, Dialog } from '@/components/ui/dialog'
import EditProfileDialog from '@/components/user-settings/EditProfileDialog.vue'

interface Props {
  user: UserOut
}

const props = defineProps<Props>()

const userInitial = computed(() => props.user.username[0].toUpperCase())

const userName = computed(() => props.user.first_name ?? props.user.username)
</script>

<template>
  <Dialog>
    <DropdownMenu>
      <DropdownMenuTrigger as-child>
        <Avatar class="avatar">
          <AvatarImage v-if="user.avatar_url" :src="user.avatar_url" />
          <AvatarFallback>{{ userInitial }}</AvatarFallback>
        </Avatar>
        <span class="sr-only">Site settings</span>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" :align-offset="2" side="bottom" :side-offset="8">
        <DropdownMenuLabel class="label">
          <span> {{ $t('welcome') }} {{ userName }} </span>
          <span class="user-email"> ({{ user.email }})</span>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DialogTrigger as-child>
          <DropdownMenuItem class="menu-item">
            <Icon icon="radix-icons:avatar" />
            {{ $t('user.profile') }}
          </DropdownMenuItem>
        </DialogTrigger>
        <DropdownMenuSeparator />

        <DropdownMenuItem>
          <Link href="/logout" class="menu-item">
            <Icon icon="radix-icons:exit" />
            {{ $t('auth.logOut') }}
          </Link>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
    <EditProfileDialog :user="user" />
  </Dialog>
</template>

<style scoped lang="postcss">
.avatar {
  cursor: pointer;
}
.label {
  width: 100%;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.user-email {
  font-size: 10px;
  color: hsl(var(--muted-foreground));
}
.menu-item {
  cursor: pointer;
  display: flex;
  width: 100%;
  align-items: center;
  gap: 8px;
}
</style>
