import * as z from 'zod'
import { useI18n } from 'vue-i18n'

function isPasswordStrong(password: string): boolean {
  const hasUppercase = /[A-Z]/.test(password)
  const hasLowercase = /[a-z]/.test(password)
  const hasNumber = /\d/.test(password)
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password)

  return hasUppercase && hasLowercase && hasNumber && hasSpecialChar
}

const MAX_FILE_SIZE = 5000000
const ACCEPTED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
export function useFormField() {
  const { t } = useI18n()
  const emailField = z
    .string()
    .min(5, t('forms.errors.minLength', { minLength: 5 }))
    .max(255, t('forms.errors.minLength', { maxLength: 5 }))
    .email(t('auth.errors.email'))

  const textField = z.string().max(255, t('forms.errors.maxLength', { maxLength: 255 }))

  const minLenTextField = z
    .string()
    .min(4, t('forms.errors.minLength', { minLength: 4 }))
    .max(255, t('forms.errors.maxLength', { maxLength: 255 }))

  const passwordField = z
    .string()
    .min(8, t('forms.errors.minLength', { minLength: 8 }))
    .max(255, t('forms.errors.maxLength', { maxLength: 255 }))

  const strongPasswordField = passwordField.refine(
    (password) => isPasswordStrong(password),
    t('auth.errors.passwordStrength')
  )
  const passwordConfirmField = z.string()
  const avatarField = z
    .any()
    .refine(
      (file) => file?.size <= MAX_FILE_SIZE,
      t('forms.errors.maxFileSize', { maxFileSize: '5MB' })
    )
    .refine(
      (file) => ACCEPTED_IMAGE_TYPES.includes(file?.type),
      t('forms.errors.acceptedImageTypes', {
        acceptedFileTypes: ACCEPTED_IMAGE_TYPES.map((type) => type.substring('image/'.length)).join(
          ','
        )
      })
    )

  return {
    emailField,
    textField,
    minLenTextField,
    passwordField,
    strongPasswordField,
    passwordConfirmField,
    avatarField
  }
}
