import './assets/index.css'

import { createApp, type DefineComponent, h } from 'vue'
import { createInertiaApp } from '@inertiajs/vue3'
import { createPinia } from 'pinia'
import { i18n } from '@/i18n/'
import AppWrapper from '@/AppWrapper.vue'

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
