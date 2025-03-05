import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Consent from "./pages/Consent";
import Baseline from "./pages/Baseline";
import Ime from "./pages/Ime";
import Crulp from "./pages/Crulp";
import Windows from "./pages/Windows";

function Test() {
  return (
    <div>
      hi
    </div>
  );
}

function App() {
  return (
    <Router>
        <Routes>
            <Route path="/" element={<Consent />} />
            <Route path="/baseline" element={<Baseline />} />
            <Route path="/crulp" element={<Crulp />} />
            <Route path="/ime" element={<Ime />} />
            <Route path="/windows" element={<Windows />} />
        </Routes>
    </Router>
  );
}

export default App
