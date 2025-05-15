import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Consent from "./pages/Consent";
import Baseline from "./pages/conditions/Baseline";
import BaselineInst from "./pages/instructions/BaselineInst";
import Windows from "./pages/conditions/Windows";
import WindowsInst from "./pages/instructions/WindowsInst";
import Ime from "./pages/conditions/Ime";
import ImeInst from "./pages/instructions/ImeInst";
import CrulpInst from "./pages/instructions/CrulpInst";
import Crulp from "./pages/conditions/Crulp";
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

            <Route path="/baseline_inst" element={<BaselineInst />} />
            <Route path="/baseline" element={<Baseline />} />

            <Route path="/windows_inst" element={<WindowsInst />} />
            <Route path="/windows" element={<Windows />} />
            
            <Route path="/ime_inst" element={<ImeInst />} />
            <Route path="/ime" element={<Ime />} />

            <Route path="/crulp_inst" element={<CrulpInst />} />
            <Route path="/crulp" element={<Crulp />} />

            <Route path="/questionnaire_inst" element={<Questionnaire />} />
            <Route path="/exit" element={<Exit />} />
            
            <Route path="/withdraw" element={<Withdraw />} />
            <Route path="/repeat" element={<Repeat />} />
            <Route path="/end" element={<End />} />
        </Routes>
    </Router>
  );
}

export default App
