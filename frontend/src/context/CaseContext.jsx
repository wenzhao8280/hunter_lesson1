import { createContext, useContext, useMemo, useState } from "react";

// CaseNext has no login system yet, so "my case" is just remembered in
// this browser via localStorage: the id of the case Case Setup created.
const STORAGE_KEY = "casenext.myCaseId";

const CaseContext = createContext(null);

export function CaseProvider({ children }) {
  const [myCaseId, setMyCaseIdState] = useState(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? Number(stored) : null;
  });

  const setMyCaseId = (caseId) => {
    setMyCaseIdState(caseId);
    if (caseId == null) {
      localStorage.removeItem(STORAGE_KEY);
    } else {
      localStorage.setItem(STORAGE_KEY, String(caseId));
    }
  };

  const value = useMemo(() => ({ myCaseId, setMyCaseId }), [myCaseId]);

  return <CaseContext.Provider value={value}>{children}</CaseContext.Provider>;
}

export function useMyCase() {
  const ctx = useContext(CaseContext);
  if (!ctx) throw new Error("useMyCase must be used within a CaseProvider");
  return ctx;
}
