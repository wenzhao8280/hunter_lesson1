import { useEffect, useState } from "react";
import { api } from "../api";
import { useMyCase } from "../context/CaseContext";
import { ErrorBanner, LoadingBanner } from "../components/StatusBanner";
import { humanize } from "../humanize";

export default function Resources() {
  const { myCaseId } = useMyCase();

  const [schools, setSchools] = useState([]);
  const [schoolId, setSchoolId] = useState("");
  const [offices, setOffices] = useState([]);
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.listSchools().then(setSchools).catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    if (!myCaseId) return;
    api
      .getCase(myCaseId)
      .then((caseData) => setSchoolId(String(caseData.school_id)))
      .catch(() => {
        // If the remembered case no longer exists, just leave the school
        // picker empty rather than surfacing an error on this page.
      });
  }, [myCaseId]);

  useEffect(() => {
    if (!schoolId) {
      setOffices([]);
      setResources([]);
      return;
    }
    setLoading(true);
    setError(null);
    Promise.all([api.listOffices(schoolId), api.listResources(schoolId)])
      .then(([officeList, resourceList]) => {
        setOffices(officeList);
        setResources(resourceList);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [schoolId]);

  return (
    <section className="page">
      <h1>Resources</h1>
      <p className="lede">Official offices and links for your school.</p>

      <label className="field">
        <span>School</span>
        <select value={schoolId} onChange={(e) => setSchoolId(e.target.value)}>
          <option value="" disabled>
            Select a school
          </option>
          {schools.map((school) => (
            <option key={school.id} value={school.id}>
              {school.name}
            </option>
          ))}
        </select>
      </label>

      {error && <ErrorBanner message={error} />}
      {loading && <LoadingBanner label="Loading resources…" />}

      {!loading && schoolId && (
        <>
          <h2>Offices</h2>
          {offices.length === 0 ? (
            <p className="hint">No offices listed for this school yet.</p>
          ) : (
            <ul className="resource-list">
              {offices.map((office) => (
                <li key={office.id} className="card">
                  <div className="resource-title">{office.name}</div>
                  {office.type && <div className="hint">{humanize(office.type)}</div>}
                  {office.description && <p>{office.description}</p>}
                  <div className="resource-links">
                    {office.website && (
                      <a href={office.website} target="_blank" rel="noreferrer">
                        Website
                      </a>
                    )}
                    {office.contact_email && (
                      <a href={`mailto:${office.contact_email}`}>
                        {office.contact_email}
                      </a>
                    )}
                    {office.contact_phone && <span>{office.contact_phone}</span>}
                  </div>
                </li>
              ))}
            </ul>
          )}

          <h2>Resources</h2>
          {resources.length === 0 ? (
            <p className="hint">No resources listed for this school yet.</p>
          ) : (
            <ul className="resource-list">
              {resources.map((resource) => (
                <li key={resource.id} className="card">
                  <div className="resource-title">
                    <a href={resource.url} target="_blank" rel="noreferrer">
                      {resource.title}
                    </a>
                  </div>
                  {resource.category && (
                    <div className="hint">{humanize(resource.category)}</div>
                  )}
                  {resource.description && <p>{resource.description}</p>}
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </section>
  );
}
