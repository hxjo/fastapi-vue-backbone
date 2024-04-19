<script setup lang="ts">
import { vAutoAnimate } from '@formkit/auto-animate/vue'
import { Button } from '@/components/ui/button'
import EmailField from '@/forms/components/EmailField.vue'
import type { UserOut } from '@/api'
import { useEditProfileForm } from '@/forms/user/composables/useEditProfileForm'
import InputField from '@/forms/components/InputField.vue'
import { router } from '@inertiajs/vue3'
import NameField from '@/forms/components/NameField.vue'
interface Props {
  user: UserOut
}

const props = defineProps<Props>()

const { form, isFormComplete, hasFormChanged } = useEditProfileForm(props.user)

const onSubmit = form.handleSubmit((values) => {
  if (values.avatar_url && typeof values.avatar_url !== 'string') {
    const formData = new FormData()
    formData.append('avatar', values.avatar_url)
    fetch(`/api/v1/users/${props.user.id}/avatar`, {
      method: 'POST',
      body: formData
    })
  }
  const changedValues = Object.fromEntries(
    Object.entries(values).filter(([key, value]) => props.user[key as keyof UserOut] !== value)
  )
  router.patch(`/api/v1/users/${props.user.id}`, { ...changedValues, avatar_url: undefined })
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
