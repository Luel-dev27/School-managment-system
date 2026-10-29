import { useState } from 'react'
import axios from 'axios'

import api from '../services/api'

interface TestResult {
  message: string
  status?: number
  isError: boolean
}

function ProtectedApiTest() {
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<TestResult | null>(null)

  const testProtectedApi = async () => {
    setIsLoading(true)
    setResult(null)

    try {
      const response = await api.get('students/')
      setResult({
        message: 'Protected API request succeeded.',
        status: response.status,
        isError: false,
      })
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        const status = error.response?.status

        if (status === 401) {
          setResult({
            message: 'Authentication is required. Please sign in again.',
            status,
            isError: true,
          })
        } else if (status === 403) {
          setResult({
            message: 'Your account does not have permission to access this endpoint.',
            status,
            isError: true,
          })
        } else if (status !== undefined) {
          setResult({
            message: 'The protected API request failed.',
            status,
            isError: true,
          })
        } else {
          setResult({
            message: 'Could not reach the server. Check that the backend is running and try again.',
            isError: true,
          })
        }
      } else {
        setResult({
          message: 'The request could not be completed. Please try again.',
          isError: true,
        })
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="protected-api-test">
      <button
        className="secondary-button"
        type="button"
        onClick={testProtectedApi}
        disabled={isLoading}
      >
        {isLoading ? 'Testing…' : 'Test Protected API'}
      </button>
      {result && (
        <p className={result.isError ? 'api-test-error' : 'api-test-success'} role="status">
          {result.message}
          {result.status !== undefined && ` (HTTP ${result.status})`}
        </p>
      )}
    </div>
  )
}

export default ProtectedApiTest
