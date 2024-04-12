<script setup lang="ts">
import { vAutoAnimate } from '@formkit/auto-animate/vue'
import { Button } from '@/components/ui/button'

import EmailField from '@/forms/components/EmailField.vue'
import { useSignupForm } from '@/forms/auth/composables/useSignupForm'
import PasswordField from '@/forms/components/PasswordField.vue'
import { OpenAPI, type UserCreate, UsersService } from '@/api'
import NameField from '@/forms/components/NameField.vue'
import { useCurrentUserStore } from '@/stores/currentUser'
import { useRouter } from 'vue-router'
import { useCookies } from '@vueuse/integrations/useCookies'
import useSafeRequest from '@/composables/useSafeRequest'

const { form, isFieldSelected, isFormComplete } = useSignupForm()
const router = useRouter()
const cookies = useCookies()

const onSubmit = form.handleSubmit(async (values) => {
  const data: UserCreate = {
    email: values.email,
    username: values.username,
    password: values.password
  }
  const response = await useSafeRequest(UsersService.createUserApiV1UsersPost, {
    requestBody: data
  })
  if (response) {
    cookies.set('access_token', response.token.access_token)
    useCurrentUserStore().setUser(response.user)
    OpenAPI.TOKEN = response.token.access_token
    await router.push('/')
  }
})
</script>

<template>
  <div class="signup-form">
    <div class="form-header">
      <h2>
        {{ $t('auth.signUp.header') }}
      </h2>
      <span>
        {{ $t('auth.signUp.subheader') }}
      </span>
    </div>
    <form @submit="onSubmit" v-auto-animate>
      <EmailField :is-field-dirty="form.isFieldDirty" />
      <div v-show="isFieldSelected('email')">
        <NameField
          :is-field-dirty="form.isFieldDirty"
          name="username"
          autocomplete="username"
          :label="$t('user.username')"
        />
        <div class="form-names">
          <NameField
            :is-field-dirty="form.isFieldDirty"
            name="first_name"
            autocomplete="given-name"
            :label="$t('user.firstName')"
          />
          <NameField
            :is-field-dirty="form.isFieldDirty"
            name="last_name"
            autocomplete="family-name"
            :label="$t('user.lastName')"
          />
        </div>
        <PasswordField :is-field-dirty="form.isFieldDirty" name="password" />
        <PasswordField :is-field-dirty="form.isFieldDirty" name="passwordConfirm" />
      </div>
      <Button type="submit" :disabled="!isFormComplete">
        {{ $t('forms.continue') }}
      </Button>
    </form>
  </div>
</template>

<style scoped lang="postcss">
.signup-form {
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

  .form-names {
    width: 100%;
    display: flex;
    gap: 16px;
  }
}
</style>
