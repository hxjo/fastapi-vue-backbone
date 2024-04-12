<script setup lang="ts">
import { vAutoAnimate } from '@formkit/auto-animate/vue'
import { Button } from '@/components/ui/button'
import { useRecoverPasswordForm } from '@/forms/auth/composables/useRecoverPasswordForm'
import EmailField from '@/forms/components/EmailField.vue'
import { ApiError, LoginService } from '@/api'
import { useToast } from '@/components/ui/toast'
import { useI18n } from 'vue-i18n'
const { form, isFormComplete } = useRecoverPasswordForm()

const { t } = useI18n()
const { toast } = useToast()

const onSubmit = form.handleSubmit(async (values) => {
  try {
    await LoginService.sendRecoverPasswordEmailApiRecoverPasswordEmailPost({
      email: values.email
    })
    toast({
      title: t('auth.success.recoveryEmail')
    })
  } catch (error) {
    if (error instanceof ApiError) {
      const errorBody = error.body as Record<string, string>
      toast({
        title: t(`serverMessages.${errorBody.message}`),
        variant: 'destructive',
        duration: 3000
      })
    }
  }
})
</script>

<template>
  <div class="recover-form">
    <div class="form-header">
      <h2>
        {{ $t('auth.recoverPassword.header') }}
      </h2>
      <span>
        {{ $t('auth.recoverPassword.subheader') }}
      </span>
    </div>
    <form @submit="onSubmit" v-auto-animate>
      <EmailField :is-field-dirty="form.isFieldDirty" />
      <Button type="submit" :disabled="!isFormComplete">
        {{ $t('auth.recoverPassword.button') }}
      </Button>
    </form>
  </div>
</template>

<style scoped lang="postcss">
.recover-form {
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

    h2 {
      font-size: 1.5rem;
      font-weight: 500;
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
