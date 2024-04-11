import type { MessageProps } from '@/messageProps'
import type { ComputedRef } from 'vue'
import { computed, watch } from 'vue'
import { useToast } from '@/components/ui/toast'
import { useI18n } from 'vue-i18n'

export function useServerMessages(message: ComputedRef<MessageProps['message']>) {
  const { toast } = useToast()
  const { t } = useI18n()
  const reactiveMessage = computed<string>(() => {
    return message.value ? message.value.content + message.value.timestamp : ''
  })
  if (reactiveMessage.value && message.value) {
    toast({
      title: t(`serverMessages.${message.value.content}`),
      variant: message.value.type === 'error' ? 'destructive' : 'default',
      duration: 3000
    })
  }

  watch(
    () => reactiveMessage.value,
    (reactiveMessage) => {
      if (reactiveMessage && message.value) {
        toast({
          title: t(`serverMessages.${message.value.content}`),
          variant: message.value.type === 'error' ? 'destructive' : 'default',
          duration: 3000
        })
      }
    }
  )
}
