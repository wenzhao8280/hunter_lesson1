import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import { useMyCase } from "../context/CaseContext";
import StepProgress from "../components/StepProgress";
import { ErrorBanner, LoadingBanner } from "../components/StatusBanner";

const STATUS_OPTIONS = ["active", "resolved", "appealed"];

export default function MyCase() {
  const { id } = useParams();
  const caseId = Number(id);
  const { setMyCaseId } = useMyCase();

  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [savingStatus, setSavingStatus] = useState(false);
  const [savingStep, setSavingStep] = useState(false);

  const [details, setDetails] = useState({
    course_name: "",
    course_code: "",
    incident_date: "",
    notice_date: "",
    student_description: "",
    has_evidence: false,
    notes: "",
  });
  const [savingDetails, setSavingDetails] = useState(false);
  const [detailsSaved, setDetailsSaved] = useState(false);

  function loadCase() {
    setLoading(true);
    setError(null);
    return api
      .getCase(caseId)
      .then((data) => {
        setCaseData(data);
        setDetails({
          course_name: data.details?.course_name ?? "",
          course_code: data.details?.course_code ?? "",
          incident_date: data.details?.incident_date ?? "",
          notice_date: data.details?.notice_date ?? "",
          student_description: data.details?.student_description ?? "",
          has_evidence: data.details?.has_evidence ?? false,
          notes: data.details?.notes ?? "",
        });
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    setMyCaseId(caseId);
    loadCase();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [caseId]);

  async function handleStatusChange(event) {
    const status = event.target.value;
    setSavingStatus(true);
    try {
      const updated = await api.updateCase(caseId, { status });
      setCaseData(updated);
    } catch (err) {
      setError(err.message);
    } finally {
      setSavingStatus(false);
    }
  }

  async function handleAdvanceStep() {
    const steps = caseData.workflow?.steps ?? [];
    const currentIndex = steps.findIndex((s) => s.id === caseData.current_step_id);
    const next = steps[currentIndex + 1];
    if (!next) return;

    setSavingStep(true);
    try {
      const updated = await api.updateCase(caseId, { current_step_id: next.id });
      setCaseData(updated);
    } catch (err) {
      setError(err.message);
    } finally {
      setSavingStep(false);
    }
  }

  async function handleDetailsSubmit(event) {
    event.preventDefault();
    setSavingDetails(true);
    setDetailsSaved(false);
    setError(null);
    try {
      await api.upsertCaseDetails(caseId, details);
      setDetailsSaved(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setSavingDetails(false);
    }
  }

  if (loading) return <LoadingBanner label="Loading your case…" />;
  if (error && !caseData) return <ErrorBanner message={error} />;
  if (!caseData) return null;

  const steps = caseData.workflow?.steps ?? [];
  const currentIndex = steps.findIndex((s) => s.id === caseData.current_step_id);
  // currentIndex is -1 when no step is set yet, in which case the "next"
  // step is steps[0] — the case just hasn't started its first step.
  const hasNextStep = currentIndex < steps.length - 1;

  return (
    <section className="page">
      <div className="page-header">
        <div>
          <h1>My Case</h1>
          <p className="subtitle">
            {caseData.school?.name} &middot; {caseData.allegation_type?.name}
          </p>
        </div>
        <Link className="button button-secondary" to={`/case/${caseId}/timeline`}>
          View timeline
        </Link>
      </div>

      {error && <ErrorBanner message={error} />}

      <div className="card">
        <div className="field-row">
          <label className="field">
            <span>Status</span>
            <select value={caseData.status} onChange={handleStatusChange} disabled={savingStatus}>
              {STATUS_OPTIONS.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
          </label>
        </div>

        {steps.length > 0 ? (
          <>
            <StepProgress steps={steps} currentStepId={caseData.current_step_id} />
            <button
              type="button"
              className="button button-primary"
              onClick={handleAdvanceStep}
              disabled={!hasNextStep || savingStep}
            >
              {savingStep
                ? "Updating…"
                : currentIndex === -1
                  ? "Start first step"
                  : "Mark current step complete"}
            </button>
          </>
        ) : (
          <p className="hint">This school hasn't published process steps yet.</p>
        )}
      </div>

      <div className="card">
        <h2>Case details</h2>
        <form className="form" onSubmit={handleDetailsSubmit}>
          <div className="field-row">
            <label className="field">
              <span>Course name</span>
              <input
                type="text"
                value={details.course_name}
                onChange={(e) => setDetails({ ...details, course_name: e.target.value })}
              />
            </label>
            <label className="field">
              <span>Course code</span>
              <input
                type="text"
                value={details.course_code}
                onChange={(e) => setDetails({ ...details, course_code: e.target.value })}
              />
            </label>
          </div>

          <div className="field-row">
            <label className="field">
              <span>Incident date</span>
              <input
                type="date"
                value={details.incident_date ?? ""}
                onChange={(e) => setDetails({ ...details, incident_date: e.target.value })}
              />
            </label>
            <label className="field">
              <span>Notice date</span>
              <input
                type="date"
                value={details.notice_date ?? ""}
                onChange={(e) => setDetails({ ...details, notice_date: e.target.value })}
              />
            </label>
          </div>

          <label className="field">
            <span>What happened, in your own words</span>
            <textarea
              rows={4}
              value={details.student_description}
              onChange={(e) =>
                setDetails({ ...details, student_description: e.target.value })
              }
            />
          </label>

          <label className="checkbox-field">
            <input
              type="checkbox"
              checked={details.has_evidence}
              onChange={(e) => setDetails({ ...details, has_evidence: e.target.checked })}
            />
            <span>I have evidence to support my case</span>
          </label>

          <label className="field">
            <span>Notes</span>
            <textarea
              rows={3}
              value={details.notes}
              onChange={(e) => setDetails({ ...details, notes: e.target.value })}
            />
          </label>

          <button type="submit" className="button button-primary" disabled={savingDetails}>
            {savingDetails ? "Saving…" : "Save details"}
          </button>
          {detailsSaved && <span className="hint">Saved.</span>}
        </form>
      </div>
    </section>
  );
}
