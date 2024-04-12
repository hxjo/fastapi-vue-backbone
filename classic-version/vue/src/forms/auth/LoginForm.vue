<script setup lang="ts">
import { vAutoAnimate } from '@formkit/auto-animate/vue'
import { Button } from '@/components/ui/button'
import { useLoginForm } from '@/forms/auth/composables/useLoginForm'
import EmailField from '@/forms/components/EmailField.vue'
import PasswordField from '@/forms/components/PasswordField.vue'
import { type Body_api_login_api_login_post, LoginService, OpenAPI } from '@/api'
import { useCookies } from '@vueuse/integrations/useCookies'
import { useRouter } from 'vue-router'
import { useCurrentUserStore } from '@/stores/currentUser'
import useSafeRequest from '@/composables/useSafeRequest'

const { form, isFormComplete } = useLoginForm()
const cookies = useCookies()
const router = useRouter()

const onSubmit = form.handleSubmit(async (values) => {
  const data: Body_api_login_api_login_post = {
    username: values.email,
    password: values.password
  }
  const response = await useSafeRequest(LoginService.apiLoginApiLoginPost, {
    formData: {
      username: data.username,
      password: data.password
    }
  })
  if (response) {
    cookies.set('access_token', response.token.access_token, { path: '/' })
    useCurrentUserStore().setUser(response.user)
    OpenAPI.TOKEN = response.token.access_token
    await router.push('/')
  }
})
</script>

<template>
  <div class="login-form">
    <div class="form-header">
      <h2>
        {{ $t('auth.logIn.header') }}
      </h2>
      <span>
        {{ $t('auth.logIn.subheader') }}
      </span>
    </div>
    <form @submit="onSubmit" v-auto-animate>
      <EmailField :is-field-dirty="form.isFieldDirty" />
      <PasswordField name="password" :is-field-dirty="form.isFieldDirty" />
      <Button type="submit" :disabled="!isFormComplete">
        {{ $t('auth.logIn.button') }}
      </Button>
    </form>
    <RouterLink to="/auth/recover-password" class="recover-password-link">{{
      $t('auth.recoverPassword.header')
    }}</RouterLink>
  </div>
</template>

<style scoped lang="postcss">
.login-form {
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 16px;

  .recover-password-link {
    font-size: 12px;
  }

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
