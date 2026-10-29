import { useState, type FormEvent } from 'react'

import { useAuth } from '../context/useAuth'

function LoginPage() {
  const { login } = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setErrorMessage('')
    setIsLoading(true)

    try {
      await login({ username, password })
    } catch {
      setErrorMessage('Unable to sign in. Check your username and password, then try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="auth-layout">
      <section className="login-card" aria-labelledby="login-title">
        <div className="brand-mark" aria-hidden="true">S</div>
        <p className="eyebrow">School Management System</p>
        <h1 id="login-title">Welcome back</h1>
        <p className="login-description">Sign in to continue to your school workspace.</p>

        <form className="login-form" onSubmit={handleSubmit}>
          <label htmlFor="username">Username</label>
          <input
            id="username"
            name="username"
            type="text"
            autoComplete="username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            required
            disabled={isLoading}
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
            disabled={isLoading}
          />

          {errorMessage && (
            <p className="form-error" role="alert">{errorMessage}</p>
          )}

          <button className="primary-button" type="submit" disabled={isLoading}>
            {isLoading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>
      </section>
    </main>
  )
}

export default LoginPage
