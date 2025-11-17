import axios from 'axios'

// API Base URL configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Configure axios defaults
axios.defaults.baseURL = API_BASE_URL
axios.defaults.headers.common['Content-Type'] = 'application/json'

export { API_BASE_URL }
export default axios
