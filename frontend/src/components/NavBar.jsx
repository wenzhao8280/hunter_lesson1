import { NavLink } from "react-router-dom";
import { useMyCase } from "../context/CaseContext";

export default function NavBar() {
  const { myCaseId } = useMyCase();

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <NavLink to="/" className="brand">
          CaseNext
        </NavLink>
        <nav className="nav-links">
          {myCaseId ? (
            <>
              <NavLink to={`/case/${myCaseId}`}>My Case</NavLink>
              <NavLink to={`/case/${myCaseId}/timeline`}>Timeline</NavLink>
            </>
          ) : (
            <NavLink to="/setup">Set Up My Case</NavLink>
          )}
          <NavLink to="/cases">Case Database</NavLink>
          <NavLink to="/resources">Resources</NavLink>
        </nav>
      </div>
    </header>
  );
}
