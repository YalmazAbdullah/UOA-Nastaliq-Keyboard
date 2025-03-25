import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Consent from "./pages/Consent";
import Baseline from "./pages/Baseline";
import Ime from "./pages/Ime";
import Crulp from "./pages/Crulp";
import Windows from "./pages/Windows";
import Questionnaire from "./pages/Questionnaire";
import Exit from "./pages/Exit";
import Withdraw from "./pages/Withdraw";


import Repeat from "./pages/Repeat";
import End from "./pages/End";

function App() {
  return (
    <Router>
        <Routes>
            <Route path="/" element={<Consent />} />
            <Route path="/baseline" element={<Baseline />} />
            <Route path="/crulp" element={<Crulp />} />
            <Route path="/ime" element={<Ime />} />
            <Route path="/windows" element={<Windows />} />
            <Route path="/questionnaire" element={<Questionnaire />} />
            <Route path="/exit" element={<Exit />} />
            
            <Route path="/withdraw" element={<Withdraw />} />
            <Route path="/repeat" element={<Repeat />} />
            <Route path="/end" element={<End />} />
        </Routes>
    </Router>
  );
}

export default App
