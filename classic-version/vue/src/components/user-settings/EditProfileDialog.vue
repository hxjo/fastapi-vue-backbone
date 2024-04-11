<script setup lang="ts">
import { DialogHeader, DialogContent, DialogTitle } from '@/components/ui/dialog'
import type { UserOut } from '@/api'
import EditProfileForm from '@/forms/user/EditProfileForm.vue'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import EditPasswordForm from '@/forms/user/EditPasswordForm.vue'

interface Props {
  user: UserOut
}

defineProps<Props>()
</script>

<template>
  <DialogContent class="edit-profile-dialog">
    <DialogHeader>
      <DialogTitle> {{ $t('user.editProfileModal.header') }}</DialogTitle>
    </DialogHeader>
    <Tabs default-value="account">
      <TabsList class="tabs-list">
        <TabsTrigger value="account"> Account </TabsTrigger>
        <TabsTrigger value="password"> Password </TabsTrigger>
      </TabsList>
      <TabsContent value="account" class="tab-content">
        <EditProfileForm :user="user" />
      </TabsContent>
      <TabsContent value="password" class="tab-content">
        <EditPasswordForm :user="user" />
      </TabsContent>
    </Tabs>
  </DialogContent>
</template>

<style lang="postcss">
.edit-profile-dialog {
  gap: 40px;

  .tabs-list {
    width: 100%;
    & > button {
      width: 50%;
    }
  }
  .tab-content {
    height: 400px;
  }
}
</style>
