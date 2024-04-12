<script setup lang="ts">
import { vAutoAnimate } from '@formkit/auto-animate/vue'
import { Button } from '@/components/ui/button'
import { useResetPasswordForm } from '@/forms/auth/composables/useResetPasswordForm'
import PasswordField from '@/forms/components/PasswordField.vue'
import { type NewPassword, LoginService } from '@/api'
import useSafeRequest from '@/composables/useSafeRequest'
import { useCurrentUserStore } from '@/stores/currentUser'
import { useI18n } from 'vue-i18n'
import { useToast } from '@/components/ui/toast'
import { useRouter } from 'vue-router'
import { useCookies } from '@vueuse/integrations/useCookies'
const { form, isFormComplete } = useResetPasswordForm()
interface Props {
  email: string
  token: string
}
const { t } = useI18n()
const { toast } = useToast()
const router = useRouter()
const cookies = useCookies()

const props = defineProps<Props>()
const onSubmit = form.handleSubmit(async (values) => {
  const data: NewPassword = {
    token: props.token,
    password: values.password
  }
  const user = await useSafeRequest(LoginService.resetPasswordApiResetPasswordPost, {
    requestBody: data
  })
  if (user) {
    cookies.set('access_token', props.token, {
      path: '/'
    })
    useCurrentUserStore().setUser(user)
    toast({
      title: t('auth.success.resetPassword')
    })
    await router.push('/')
  }
})
</script>

<template>
  <div class="reset-form">
    <div class="form-header">
      <h2>
        {{ $t('auth.resetPassword.header', { email }) }}
      </h2>
      <span>
        {{ $t('auth.resetPassword.subheader') }}
      </span>
    </div>
    <form @submit="onSubmit" v-auto-animate>
      <PasswordField :is-field-dirty="form.isFieldDirty" name="password" />
      <PasswordField :is-field-dirty="form.isFieldDirty" name="passwordConfirm" />
      <Button type="submit" :disabled="!isFormComplete">
        {{ $t('auth.resetPassword.button') }}
      </Button>
    </form>
  </div>
</template>

<style scoped lang="postcss">
.reset-form {
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 16px;

  .form-header {
    display: flex;
    flex-direction: column;
    gap: 4px;
    max-width: 600px;

    h2 {
      font-size: 1.5rem;
      font-weight: 500;
      text-align: center;
    }
    span {
      text-align: center;
    }
  }
  form,
  form > div {
    display: flex;
    flex-direction: column;
    width: 350px;

    gap: 16px;
  }
}
</style>
