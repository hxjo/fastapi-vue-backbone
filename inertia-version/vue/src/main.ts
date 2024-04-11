import './assets/index.css'

import { createApp, type DefineComponent, h } from 'vue'
import { createInertiaApp } from '@inertiajs/vue3'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import { FrenchTranslationRecord } from '@/i18n/fr'
import { EnglishTranslationRecord } from '@/i18n/en'
import AppWrapper from '@/AppWrapper.vue'
import { useCookies } from '@vueuse/integrations/useCookies'

const cookies = useCookies()

const i18n = createI18n({
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

createInertiaApp({
  resolve: (name: string) => {
    const pages = import.meta.glob('./Pages/**/*.vue', { eager: true })
    return pages[`./Pages/${name}.vue`] as DefineComponent
  },
  setup({ el, App, props, plugin }: any) {
    createApp({ render: () => h(AppWrapper, null, { default: () => h(App, props) }) })
      .use(plugin)
      .use(createPinia())
      .use(i18n)
      .mount(el)
  }
})
