export interface LoginCredentials {
  username: string
  password: string
}

export interface LoginResponse {
  token: string
  username: string
  groups: string[]
}

export interface AuthUser {
  username: string
  groups: string[]
}