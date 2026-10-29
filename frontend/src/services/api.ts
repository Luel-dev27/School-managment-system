import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
})

let authToken: string | null = null

export const setAuthToken = (token: string | null) => {
  authToken = token
}

api.interceptors.request.use((config) => {
  if (authToken) {
    config.headers.set('Authorization', `Token ${authToken}`)
  } else {
    config.headers.delete('Authorization')
  }

  return config
})

export default api
