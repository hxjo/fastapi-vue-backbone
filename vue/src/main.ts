import './assets/index.css'

import { createApp, h } from 'vue'
import { createInertiaApp } from '@inertiajs/vue3'
import { createPinia } from 'pinia'


createInertiaApp({
  resolve: (name: string) => {
    const pages = import.meta.glob('./Pages/**/*.vue', { eager: true })
    return pages[`./Pages/${name}.vue`]
  },
  setup({ el, App, props, plugin }: any) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .use(createPinia())
      .mount(el)
  },
})

