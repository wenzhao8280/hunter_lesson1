import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import { ErrorBanner, LoadingBanner } from "../components/StatusBanner";

const SOURCE_OPTIONS = ["student", "official"];

const emptyEvent = {
  title: "",
  event_type: "",
  event_date: "",
  source: "student",
  description: "",
};

export default function Timeline() {
  const { id } = useParams();
  const caseId = Number(id);

  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [form, setForm] = useState(emptyEvent);
  const [submitting, setSubmitting] = useState(false);

  function loadEvents() {
    setLoading(true);
    setError(null);
    return api
      .listCaseEvents(caseId)
      .then(setEvents)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    loadEvents();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [caseId]);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!form.title || !form.event_date) return;

    setSubmitting(true);
    setError(null);
    try {
      await api.createCaseEvent(caseId, {
        ...form,
        event_date: new Date(form.event_date).toISOString(),
      });
      setForm(emptyEvent);
      await loadEvents();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="page">
      <div className="page-header">
        <div>
          <h1>Timeline</h1>
          <p className="subtitle">Everything that's happened in your case, in order.</p>
        </div>
        <Link className="button button-secondary" to={`/case/${caseId}`}>
          Back to my case
        </Link>
      </div>

      {error && <ErrorBanner message={error} />}

      <div className="card">
        <h2>Add an event</h2>
        <form className="form" onSubmit={handleSubmit}>
          <div className="field-row">
            <label className="field">
              <span>Title</span>
              <input
                type="text"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
                required
              />
            </label>
            <label className="field">
              <span>When</span>
              <input
                type="datetime-local"
                value={form.event_date}
                onChange={(e) => setForm({ ...form, event_date: e.target.value })}
                required
              />
            </label>
          </div>

          <div className="field-row">
            <label className="field">
              <span>Type</span>
              <input
                type="text"
                placeholder="e.g. meeting, notice, deadline"
                value={form.event_type}
                onChange={(e) => setForm({ ...form, event_type: e.target.value })}
              />
            </label>
            <label className="field">
              <span>Logged by</span>
              <select
                value={form.source}
                onChange={(e) => setForm({ ...form, source: e.target.value })}
              >
                {SOURCE_OPTIONS.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <label className="field">
            <span>Description</span>
            <textarea
              rows={3}
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
            />
          </label>

          <button type="submit" className="button button-primary" disabled={submitting}>
            {submitting ? "Adding…" : "Add event"}
          </button>
        </form>
      </div>

      {loading ? (
        <LoadingBanner label="Loading timeline…" />
      ) : events.length === 0 ? (
        <p className="hint">No events yet.</p>
      ) : (
        <ol className="timeline">
          {events.map((event) => (
            <li key={event.id} className="timeline-entry">
              <div className="timeline-date">
                {new Date(event.event_date).toLocaleString()}
              </div>
              <div className="timeline-body">
                <div className="timeline-title">
                  {event.title}
                  <span className={`badge badge-${event.source}`}>{event.source}</span>
                </div>
                {event.event_type && (
                  <div className="timeline-type">{event.event_type}</div>
                )}
                {event.description && <p>{event.description}</p>}
              </div>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
