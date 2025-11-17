import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './style.css'
import { registerServiceWorker } from './registerServiceWorker'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

// Register service worker in production
if (import.meta.env.PROD) {
  registerServiceWorker()
}
