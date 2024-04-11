import * as z from 'zod'
import { useFormField } from '@/forms/composables/useFormField'
import { useBaseForm } from '@/forms/composables/useBaseForm'

export function useLoginForm() {
  const { emailField, passwordField } = useFormField()
  const zodSchema = z.object({
    email: emailField,
    password: passwordField
  })

  const { form, isFormComplete } = useBaseForm(zodSchema)

  return {
    form,
    isFormComplete
  }
}
