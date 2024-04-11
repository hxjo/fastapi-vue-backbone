import * as z from 'zod'
import { useFormField } from '@/forms/composables/useFormField'
import { useI18n } from 'vue-i18n'
import { useBaseForm } from '@/forms/composables/useBaseForm'

export function useSignupForm() {
  const { t } = useI18n()
  const { emailField, textField, minLenTextField, strongPasswordField, passwordConfirmField } =
    useFormField()
  const zodSchema = z
    .object({
      email: emailField,
      username: minLenTextField,
      first_name: textField.optional(),
      last_name: textField.optional(),
      password: strongPasswordField,
      passwordConfirm: passwordConfirmField
    })
    .refine((data) => data.password === data.passwordConfirm, {
      message: t('auth.errors.passwordMatch'),
      path: ['passwordConfirm']
    })

  const { form, isFieldSelected, isFormComplete } = useBaseForm(zodSchema)
  return {
    form,
    isFieldSelected,
    isFormComplete
  }
}
