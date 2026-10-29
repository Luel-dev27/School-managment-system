import { createContext } from 'react'

import type { AuthUser, LoginCredentials } from '../types/auth'

export interface AuthContextType {
  user: AuthUser | null
  token: string | null
  login: (credentials: LoginCredentials) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export default AuthContext
