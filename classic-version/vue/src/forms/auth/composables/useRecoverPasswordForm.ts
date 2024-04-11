import * as z from 'zod'
import { useFormField } from '@/forms/composables/useFormField'
import { useBaseForm } from '@/forms/composables/useBaseForm'

export function useRecoverPasswordForm() {
  const { emailField } = useFormField()
  const zodSchema = z.object({
    email: emailField
  })

  const { form, isFormComplete } = useBaseForm(zodSchema)

  return {
    form,
    isFormComplete
  }
}
