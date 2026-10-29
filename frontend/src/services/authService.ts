import api from './api'
import type { LoginCredentials, LoginResponse } from '../types/auth'

export const login = async (
  credentials: LoginCredentials,
): Promise<LoginResponse> => {
  const response = await api.post<LoginResponse>(
    'accounts/login/',
    credentials,
  )

  return response.data
}