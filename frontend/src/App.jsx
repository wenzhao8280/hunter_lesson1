import { Route, Routes } from "react-router-dom";
import NavBar from "./components/NavBar";
import Landing from "./pages/Landing";
import CaseSetup from "./pages/CaseSetup";
import MyCase from "./pages/MyCase";
import Timeline from "./pages/Timeline";
import CaseDatabase from "./pages/CaseDatabase";
import Resources from "./pages/Resources";

export default function App() {
  return (
    <>
      <NavBar />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/setup" element={<CaseSetup />} />
          <Route path="/case/:id" element={<MyCase />} />
          <Route path="/case/:id/timeline" element={<Timeline />} />
          <Route path="/cases" element={<CaseDatabase />} />
          <Route path="/resources" element={<Resources />} />
        </Routes>
      </main>
    </>
  );
}
