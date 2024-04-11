import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import { useForm } from 'vee-validate'
import { computed } from 'vue'

export function useBaseForm<T extends z.ZodRawShape>(
  zodSchema: z.ZodObject<T> | z.ZodEffects<z.ZodObject<T>>,
  initialValues?: Record<string, any>
) {
  const loginFormSchema = toTypedSchema(zodSchema)
  const form = useForm({
    validationSchema: loginFormSchema,
    initialValues: initialValues ?? {}
  })

  function isFieldSelected(fieldName: keyof typeof form.values): boolean {
    return Boolean(!form.errors.value[fieldName] && form.values[fieldName])
  }

  const isFormComplete = computed(() => {
    const hasErrors =
      (Object.keys(form.errors.value) as Array<keyof typeof form.errors.value>).find(
        (key) => form.errors.value[key]
      ) !== undefined
    const hasMissingValues =
      (Object.keys(form.values) as Array<keyof typeof form.values>).find((key) => {
        return (
          !(zodSchema instanceof z.ZodObject && zodSchema.shape[key] instanceof z.ZodOptional) &&
          (form.values[key] === '' || !form.values[key])
        )
      }) !== undefined

    return !hasErrors && !hasMissingValues
  })

  const hasFormChanged = computed(() => {
    return Object.keys(form.values).some((key) => form.values[key] !== initialValues?.[key])
  })

  return {
    form,
    isFormComplete,
    hasFormChanged,
    isFieldSelected
  }
}
