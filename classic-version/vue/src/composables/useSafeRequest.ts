import { useToast } from '@/components/ui/toast'
import { i18n } from '@/i18n'
import { ApiError } from '@/api'
import { useRouter } from 'vue-router'

export default async function useSafeRequest<T extends (...args: any[]) => any>(
  func: T,
  ...args: Parameters<T>
): Promise<ReturnType<T> | null> {
  const router = useRouter()
  try {
    return await func(...args)
  } catch (error) {
    if (error instanceof ApiError) {
      const { toast } = useToast()
      const { t } = i18n.global
      if (error.status === 401) {
        await router.push({ path: '/auth/login' })
      } else if (error.status !== 500) {
        const errorBody = error.body as Record<string, string>
        toast({
          title: t(`serverMessages.${errorBody.message}`),
          variant: 'destructive',
          duration: 3000
        })
      } else {
        toast({
          title: t('serverMessages.internalServerError'),
          variant: 'destructive',
          duration: 3000
        })
      }
    }
    return null
  }
}
