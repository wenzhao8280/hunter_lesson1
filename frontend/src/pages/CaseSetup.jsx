import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";
import { useMyCase } from "../context/CaseContext";
import { ErrorBanner, LoadingBanner } from "../components/StatusBanner";

export default function CaseSetup() {
  const navigate = useNavigate();
  const { setMyCaseId } = useMyCase();

  const [schools, setSchools] = useState([]);
  const [schoolId, setSchoolId] = useState("");
  const [workflows, setWorkflows] = useState([]);
  const [workflowId, setWorkflowId] = useState("");
  const [allegationTypes, setAllegationTypes] = useState([]);
  const [allegationTypeId, setAllegationTypeId] = useState("");

  const [loadingSchools, setLoadingSchools] = useState(true);
  const [loadingSchoolData, setLoadingSchoolData] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .listSchools()
      .then(setSchools)
      .catch((err) => setError(err.message))
      .finally(() => setLoadingSchools(false));
  }, []);

  useEffect(() => {
    if (!schoolId) {
      setWorkflows([]);
      setAllegationTypes([]);
      return;
    }
    setLoadingSchoolData(true);
    setError(null);
    Promise.all([
      api.listWorkflows(schoolId),
      api.listAllegationTypes(schoolId),
    ])
      .then(([workflowList, allegationTypeList]) => {
        setWorkflows(workflowList);
        setAllegationTypes(allegationTypeList);
        setWorkflowId(workflowList[0]?.id ?? "");
        setAllegationTypeId(allegationTypeList[0]?.id ?? "");
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoadingSchoolData(false));
  }, [schoolId]);

  const canSubmit = schoolId && workflowId && allegationTypeId && !submitting;

  async function handleSubmit(event) {
    event.preventDefault();
    if (!canSubmit) return;

    setSubmitting(true);
    setError(null);
    try {
      const created = await api.createCase({
        school_id: Number(schoolId),
        workflow_id: Number(workflowId),
        allegation_type_id: Number(allegationTypeId),
      });
      setMyCaseId(created.id);
      navigate(`/case/${created.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (loadingSchools) return <LoadingBanner label="Loading schools…" />;

  return (
    <section className="page">
      <h1>Set up my case</h1>
      <p className="lede">
        Tell us your school and what you've been accused of. You can add more
        details once your case is created.
      </p>

      {error && <ErrorBanner message={error} />}

      <form className="card form" onSubmit={handleSubmit}>
        <label className="field">
          <span>School</span>
          <select
            value={schoolId}
            onChange={(event) => setSchoolId(event.target.value)}
            required
          >
            <option value="" disabled>
              Select your school
            </option>
            {schools.map((school) => (
              <option key={school.id} value={school.id}>
                {school.name}
              </option>
            ))}
          </select>
        </label>

        {loadingSchoolData && <LoadingBanner label="Loading school info…" />}

        {!loadingSchoolData && schoolId && workflows.length > 1 && (
          <label className="field">
            <span>Process</span>
            <select
              value={workflowId}
              onChange={(event) => setWorkflowId(event.target.value)}
              required
            >
              {workflows.map((workflow) => (
                <option key={workflow.id} value={workflow.id}>
                  {workflow.name}
                </option>
              ))}
            </select>
          </label>
        )}

        {!loadingSchoolData && schoolId && allegationTypes.length > 0 && (
          <label className="field">
            <span>What are you accused of?</span>
            <select
              value={allegationTypeId}
              onChange={(event) => setAllegationTypeId(event.target.value)}
              required
            >
              {allegationTypes.map((allegationType) => (
                <option key={allegationType.id} value={allegationType.id}>
                  {allegationType.name}
                </option>
              ))}
            </select>
          </label>
        )}

        {!loadingSchoolData && schoolId && allegationTypes.length === 0 && (
          <p className="hint">
            This school doesn't have any allegation types set up yet.
          </p>
        )}

        <button type="submit" className="button button-primary" disabled={!canSubmit}>
          {submitting ? "Creating…" : "Create my case"}
        </button>
      </form>
    </section>
  );
}
