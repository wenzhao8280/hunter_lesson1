import { Link } from "react-router-dom";
import { useMyCase } from "../context/CaseContext";

export default function Landing() {
  const { myCaseId } = useMyCase();

  return (
    <section className="page landing">
      <h1>Know what happens next.</h1>
      <p className="lede">
        CaseNext helps you understand where you are in your school's academic
        misconduct process, what may happen next, what to prepare, and what
        other students have experienced in similar cases.
      </p>
      <p className="lede">
        Every school uses its own terms, offices, and steps. CaseNext never
        forces a generic process onto your school — you'll see your school's
        actual wording, not a guess.
      </p>
      <div className="cta-row">
        {myCaseId ? (
          <Link className="button button-primary" to={`/case/${myCaseId}`}>
            Continue to my case
          </Link>
        ) : (
          <Link className="button button-primary" to="/setup">
            Set up my case
          </Link>
        )}
        <Link className="button button-secondary" to="/cases">
          Browse the case database
        </Link>
      </div>
    </section>
  );
}
