import { useCookies } from '@vueuse/integrations/useCookies'
import { createI18n } from 'vue-i18n'
import { FrenchTranslationRecord } from '@/i18n/fr'
import { EnglishTranslationRecord } from '@/i18n/en'

const cookies = useCookies()

export const i18n = createI18n({
  locale: cookies.get('locale') || 'en',
  legacy: false,
  messages: {
    fr: {
      ...FrenchTranslationRecord
    },
    en: {
      ...EnglishTranslationRecord
    }
  }
})
