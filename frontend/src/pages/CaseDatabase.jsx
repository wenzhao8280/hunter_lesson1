import { useEffect, useState } from "react";
import { api } from "../api";
import { ErrorBanner, LoadingBanner } from "../components/StatusBanner";

const STATUS_OPTIONS = ["active", "resolved", "appealed"];

export default function CaseDatabase() {
  const [schools, setSchools] = useState([]);
  const [schoolId, setSchoolId] = useState("");
  const [status, setStatus] = useState("");

  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.listSchools().then(setSchools).catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    setLoading(true);
    setError(null);
    const params = {};
    if (schoolId) params.school_id = schoolId;
    if (status) params.status = status;

    api
      .listCases(params)
      .then(setCases)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [schoolId, status]);

  return (
    <section className="page">
      <h1>Case Database</h1>
      <p className="lede">
        Anonymized cases other students have logged, so you can see what
        similar situations looked like.
      </p>

      <div className="filter-row">
        <label className="field">
          <span>School</span>
          <select value={schoolId} onChange={(e) => setSchoolId(e.target.value)}>
            <option value="">All schools</option>
            {schools.map((school) => (
              <option key={school.id} value={school.id}>
                {school.name}
              </option>
            ))}
          </select>
        </label>
        <label className="field">
          <span>Status</span>
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="">All statuses</option>
            {STATUS_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </label>
      </div>

      {error && <ErrorBanner message={error} />}

      {loading ? (
        <LoadingBanner label="Loading cases…" />
      ) : cases.length === 0 ? (
        <p className="hint">No cases match those filters.</p>
      ) : (
        <ul className="case-list">
          {cases.map((c) => (
            <li key={c.id} className="card case-card">
              <div className="case-card-header">
                <span className="school-name">{c.school_name}</span>
                <span className={`badge badge-status-${c.status}`}>{c.status}</span>
              </div>
              <div className="case-card-body">
                <div>{c.allegation_type_name}</div>
                <div className="hint">
                  {c.workflow_name}
                  {c.current_step_name ? ` — ${c.current_step_name}` : ""}
                </div>
              </div>
              <div className="case-card-footer">
                Opened {new Date(c.created_at).toLocaleDateString()}
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
