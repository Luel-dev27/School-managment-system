import { useEffect, useState } from 'react'
import axios from 'axios'

import { useAuth } from './context/useAuth'
import ProtectedApiTest from './components/ProtectedApiTest'
import LoginPage from './pages/LoginPage'
import api from './services/api'

interface StudentRecord {
  id: number
  first_name: string
  last_name: string
  student_id: string
  grade_level: number | null
  status: string
}

function StudentsView({ onBack }: { onBack: () => void }) {
  const [students, setStudents] = useState<StudentRecord[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState('')

  useEffect(() => {
    let isCurrent = true

    const loadStudents = async () => {
      try {
        const response = await api.get<StudentRecord[]>('students/')
        if (isCurrent) {
          setStudents(response.data)
        }
      } catch (error: unknown) {
        if (!isCurrent) return

        if (axios.isAxiosError(error)) {
          const status = error.response?.status
          if (status === 401) {
            setErrorMessage('Your session could not be authenticated. Please sign in again.')
          } else if (status === 403) {
            setErrorMessage('Your account does not have permission to view students.')
          } else if (status !== undefined) {
            setErrorMessage(`Students could not be loaded (HTTP ${status}).`)
          } else {
            setErrorMessage('Could not connect to the server. Check that the backend is running.')
          }
        } else {
          setErrorMessage('Students could not be loaded. Please try again.')
        }
      } finally {
        if (isCurrent) {
          setIsLoading(false)
        }
      }
    }

    void loadStudents()

    return () => {
      isCurrent = false
    }
  }, [])

  return (
    <main className="student-layout">
      <section className="student-page" aria-labelledby="students-title">
        <button className="back-button" type="button" onClick={onBack}>
          <span aria-hidden="true">←</span> Back to welcome
        </button>
        <p className="eyebrow">School Management System</p>
        <h1 id="students-title">Students</h1>
        <p className="login-description">View student records available to your account.</p>

        {isLoading ? (
          <p className="student-message" role="status">Loading students…</p>
        ) : errorMessage ? (
          <p className="student-message api-test-error" role="alert">{errorMessage}</p>
        ) : students.length === 0 ? (
          <p className="student-message">No student records found.</p>
        ) : (
          <div className="student-table-wrap">
            <table className="student-table">
              <thead>
                <tr>
                  <th scope="col">Student ID</th>
                  <th scope="col">Name</th>
                  <th scope="col">Grade</th>
                  <th scope="col">Status</th>
                </tr>
              </thead>
              <tbody>
                {students.map((student) => (
                  <tr key={student.id}>
                    <td>{student.student_id}</td>
                    <td>{student.first_name} {student.last_name}</td>
                    <td>{student.grade_level === null ? '—' : student.grade_level}</td>
                    <td><span className="student-status">{student.status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </main>
  )
}

function App() {
  const { user, logout } = useAuth()
  const [activeView, setActiveView] = useState<'welcome' | 'students'>('welcome')

  if (!user) {
    return <LoginPage />
  }

  if (activeView === 'students') {
    return <StudentsView onBack={() => setActiveView('welcome')} />
  }

  return (
    <main className="auth-layout">
      <section className="login-card welcome-card" aria-labelledby="welcome-title">
        <div className="brand-mark" aria-hidden="true">S</div>
        <p className="eyebrow">School Management System</p>
        <h1 id="welcome-title">Welcome, {user.username}</h1>
        <p className="login-description">You are signed in to your school workspace.</p>
        <div className="group-summary">
          <h2>Your groups</h2>
          {user.groups.length > 0 ? (
            <ul>
              {user.groups.map((group) => <li key={group}>{group}</li>)}
            </ul>
          ) : (
            <p>No groups are assigned to your account.</p>
          )}
        </div>
        <button
          className="primary-button"
          type="button"
          onClick={() => setActiveView('students')}
        >
          View students
        </button>
        <ProtectedApiTest />
        <button className="secondary-button" type="button" onClick={() => {
          setActiveView('welcome')
          logout()
        }}>
          Log out
        </button>
      </section>
    </main>
  )
}

export default App
