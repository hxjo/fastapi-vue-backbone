import * as z from 'zod'
import { useFormField } from '@/forms/composables/useFormField'
import { useBaseForm } from '@/forms/composables/useBaseForm'

export function useResetPasswordForm() {
  const { strongPasswordField, passwordConfirmField } = useFormField()
  const zodSchema = z.object({
    password: strongPasswordField,
    passwordConfirm: passwordConfirmField
  })

  const { form, isFormComplete } = useBaseForm(zodSchema)

  return {
    form,
    isFormComplete
  }
}
