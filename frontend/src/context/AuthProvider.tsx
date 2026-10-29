import { useState, type ReactNode } from 'react'

import AuthContext from './authContext'
import { login as loginRequest } from '../services/authService'
import { setAuthToken } from '../services/api'
import type { AuthUser, LoginCredentials } from '../types/auth'

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [token, setToken] = useState<string | null>(null)

  const login = async (credentials: LoginCredentials) => {
    const data = await loginRequest(credentials)

    setAuthToken(data.token)
    setToken(data.token)
    setUser({
      username: data.username,
      groups: data.groups,
    })
  }

  const logout = () => {
    setAuthToken(null)
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
