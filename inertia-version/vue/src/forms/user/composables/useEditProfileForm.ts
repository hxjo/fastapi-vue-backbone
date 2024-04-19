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
    avatar_url: avatarField.optional()
  })

  const validInitialValues = {
    ...initialValues,
    avatar_url: initialValues.avatar_url ?? '',
    first_name: initialValues.first_name ?? '',
    last_name: initialValues.last_name ?? ''
  }

  const { form, isFormComplete, hasFormChanged } = useBaseForm(zodSchema, validInitialValues)

  return {
    form,
    isFormComplete,
    hasFormChanged
  }
}
