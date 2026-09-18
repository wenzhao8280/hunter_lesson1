const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000/api";

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  const body = await res.json().catch(() => null);

  if (!res.ok) {
    const message = body?.error || `Request failed with status ${res.status}`;
    throw new Error(message);
  }

  return body;
}

export const api = {
  listSchools: () => request("/schools"),
  getSchool: (schoolId) => request(`/schools/${schoolId}`),
  listOffices: (schoolId) => request(`/schools/${schoolId}/offices`),
  listTerminology: (schoolId) => request(`/schools/${schoolId}/terminology`),
  listWorkflows: (schoolId) => request(`/schools/${schoolId}/workflows`),
  listAllegationTypes: (schoolId) =>
    request(`/schools/${schoolId}/allegation-types`),
  listResources: (schoolId) => request(`/schools/${schoolId}/resources`),

  listCases: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return request(`/cases${query ? `?${query}` : ""}`);
  },
  createCase: (data) =>
    request("/cases", { method: "POST", body: JSON.stringify(data) }),
  getCase: (caseId) => request(`/cases/${caseId}`),
  updateCase: (caseId, data) =>
    request(`/cases/${caseId}`, { method: "PATCH", body: JSON.stringify(data) }),

  upsertCaseDetails: (caseId, data) =>
    request(`/cases/${caseId}/details`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  listCaseEvents: (caseId) => request(`/cases/${caseId}/events`),
  createCaseEvent: (caseId, data) =>
    request(`/cases/${caseId}/events`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  listCaseOutcomes: (caseId) => request(`/cases/${caseId}/outcomes`),
  createCaseOutcome: (caseId, data) =>
    request(`/cases/${caseId}/outcomes`, {
      method: "POST",
      body: JSON.stringify(data),
    }),
};
