const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options.headers },
  })
  const body = await response.json().catch(() => null)
  if (!response.ok) throw new Error(body?.detail || 'Something went wrong. Please try again.')
  return body
}

const authenticated = (token) => ({ Authorization: `Bearer ${token}` })

export const signup = (data) => request('/auth/signup', { method: 'POST', body: JSON.stringify(data) })
export const login = (data) => request('/auth/login', { method: 'POST', body: JSON.stringify(data) })
export const createFeedbackPage = (data, token) => request('/feedback-pages', { method: 'POST', headers: authenticated(token), body: JSON.stringify(data) })
export const getFeedbackPages = (token) => request('/feedback-pages', { headers: authenticated(token) })
export const setFeedbackStatus = (pageId, accepting_feedback, token) => request(`/feedback-pages/${pageId}/status`, { method: 'PATCH', headers: authenticated(token), body: JSON.stringify({ accepting_feedback }) })
export const getPublicFeedbackPage = (username, pageId) => request(`/feedback/${encodeURIComponent(username)}/${pageId}`)
export const submitFeedback = (username, pageId, data) => request(`/feedback/${encodeURIComponent(username)}/${pageId}`, { method: 'POST', body: JSON.stringify(data) })
export const getFeedback = (pageId, token) => request(`/feedback/pages/${pageId}/feedback`, { headers: authenticated(token) })
