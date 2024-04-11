import * as z from 'zod'
import { useFormField } from '@/forms/composables/useFormField'
import { useBaseForm } from '@/forms/composables/useBaseForm'

export function useEditPasswordForm() {
  const { strongPasswordField, passwordConfirmField } = useFormField()
  const zodSchema = z.object({
    password: strongPasswordField,
    passwordConfirm: passwordConfirmField
  })

  const { form, isFormComplete, hasFormChanged } = useBaseForm(zodSchema)

  return {
    form,
    isFormComplete,
    hasFormChanged
  }
}
