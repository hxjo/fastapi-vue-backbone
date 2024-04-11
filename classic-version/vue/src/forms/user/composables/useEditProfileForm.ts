import * as z from 'zod'
import { useFormField } from '@/forms/composables/useFormField'
import { useBaseForm } from '@/forms/composables/useBaseForm'
import type { UserOut } from '@/api'

export function useEditProfileForm(initialValues: UserOut) {
  const { emailField, textField, minLenTextField, avatarField } = useFormField()
  const zodSchema = z.object({
    email: emailField,
    username: minLenTextField,
    first_name: textField.optional(),
    last_name: textField.optional(),
    avatar: avatarField.optional()
  })

  const validInitialValues = {
    ...initialValues,
    avatar_url: initialValues.avatar_url ?? ''
  }

  const { form, isFormComplete, hasFormChanged } = useBaseForm(zodSchema, validInitialValues)

  return {
    form,
    isFormComplete,
    hasFormChanged
  }
}
