<script setup lang="ts">
import { vAutoAnimate } from '@formkit/auto-animate/vue'
import { Button } from '@/components/ui/button'
import { type UserOut, UsersService } from '@/api'
import { useEditPasswordForm } from '@/forms/user/composables/useEditPasswordForm'

import PasswordField from '@/forms/components/PasswordField.vue'
import useSafeRequest from '@/composables/useSafeRequest'
interface Props {
  user: UserOut
}

const props = defineProps<Props>()
const { form, isFormComplete, hasFormChanged } = useEditPasswordForm()

const onSubmit = form.handleSubmit(async (values) => {
  await useSafeRequest(UsersService.updateUserApiV1UsersUserIdPatch, {
    userId: props.user.id,
    requestBody: {
      password: values.password
    }
  })
})
</script>

<template>
  <form @submit="onSubmit" v-auto-animate class="edit-password-form">
    <PasswordField name="password" :is-field-dirty="() => true" />
    <PasswordField name="passwordConfirm" :is-field-dirty="() => true" />
    <Button type="submit" :disabled="!isFormComplete || !hasFormChanged">
      {{ $t('forms.save') }}
    </Button>
  </form>
</template>

<style scoped lang="postcss">
.edit-password-form {
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
}
</style>
