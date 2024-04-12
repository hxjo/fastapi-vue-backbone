<script setup lang="ts">
import { vAutoAnimate } from '@formkit/auto-animate/vue'
import { Button } from '@/components/ui/button'
import EmailField from '@/forms/components/EmailField.vue'
import { type UserOut, UsersService } from '@/api'
import { useEditProfileForm } from '@/forms/user/composables/useEditProfileForm'
import InputField from '@/forms/components/InputField.vue'
import NameField from '@/forms/components/NameField.vue'
import useSafeRequest from '@/composables/useSafeRequest'
import { useCurrentUserStore } from '@/stores/currentUser'
import { useToast } from '@/components/ui/toast'
import { useI18n } from 'vue-i18n'
interface Props {
  user: UserOut
}

const props = defineProps<Props>()
const { form, isFormComplete, hasFormChanged } = useEditProfileForm(props.user)
const { toast } = useToast()
const { t } = useI18n()

const onSubmit = form.handleSubmit(async (values) => {
  if (values.avatar_url && typeof values.avatar_url !== 'string') {
    await useSafeRequest(UsersService.setUserAvatarApiV1UsersUserIdAvatarPost, {
      userId: props.user.id,
      formData: {
        avatar: values.avatar_url
      }
    })
  }
  const changedValues = Object.fromEntries(
    Object.entries(values).filter(([key, value]) => props.user[key as keyof UserOut] !== value)
  )
  const hasChanged = Object.keys(changedValues).length
  if (hasChanged) {
    const user = await useSafeRequest(UsersService.updateUserApiV1UsersUserIdPatch, {
      userId: props.user.id,
      requestBody: changedValues
    })
    if (user) {
      useCurrentUserStore().setUser(user)
    }
  }
  if (hasChanged || values.avatar_url) {
    toast({
      title: t('user.success.update'),
      duration: 3000
    })
  }
})
</script>

<template>
  <form @submit="onSubmit" v-auto-animate class="edit-profile-form">
    <EmailField :is-field-dirty="() => true" class="field" />
    <NameField
      :is-field-dirty="() => true"
      name="username"
      autocomplete="username"
      :label="$t('user.username')"
    />
    <div class="form-names">
      <NameField
        autocomplete="given-name"
        name="first_name"
        :is-field-dirty="() => true"
        :label="$t('user.firstName')"
      />
      <NameField
        autocomplete="family-name"
        name="last_name"
        :is-field-dirty="() => true"
        :label="$t('user.lastName')"
      />
    </div>
    <InputField
      :is-field-dirty="() => true"
      :label="$t('user.editProfileModal.avatar')"
      fieldName="avatar_url"
    />
    <Button type="submit" :disabled="!isFormComplete || !hasFormChanged">
      {{ $t('forms.save') }}
    </Button>
  </form>
</template>

<style scoped lang="postcss">
.edit-profile-form {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: start;
  gap: 16px;

  button {
    align-self: end;
    margin-top: auto;
  }
  .form-names {
    width: 100%;
    display: flex;
    gap: 16px;
    justify-content: space-between;
  }
}
</style>
