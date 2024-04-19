import { watch } from 'vue'
import { useToast } from '@/components/ui/toast'
import { useI18n } from 'vue-i18n'
import { usePage } from '@inertiajs/vue3'

interface ServerMessage {
  message: string
  category: 'error' | 'message'
}

export function useServerMessages() {
  const { toast } = useToast()
  const { t } = useI18n()
  const page = usePage()

  if (page.props && (page.props.messages as ServerMessage[]).length > 0) {
    ;(page.props.messages as ServerMessage[]).forEach((message: ServerMessage) => {
      toast({
        title: t(`serverMessages.${message.message}`),
        variant: message.category === 'error' ? 'destructive' : 'default',
        duration: 3000
      })
    })
  }

  watch(
    () => page.props?.messages,
    (serverMessages) => {
      if ((serverMessages as ServerMessage[]).length > 0) {
        ;(serverMessages as ServerMessage[]).forEach((message: ServerMessage) => {
          toast({
            title: t(`serverMessages.${message.message}`),
            variant: message.category === 'error' ? 'destructive' : 'default',
            duration: 3000
          })
        })
      }
    }
  )
}
