import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import RainfallMapPage from "./pages/RainfallMapPage";
import Forecast from "./pages/Forecast";
import ModelPerformance from "./pages/ModelPerformance";
import Reports from "./pages/Reports";
import About from "./pages/About";
import AppShell from "./components/layout/AppShell";

function App() {
  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/rainfall-map"
            element={<RainfallMapPage />}
          />

          <Route
            path="/forecast"
            element={<Forecast />}
          />

          <Route
            path="/model-performance"
            element={<ModelPerformance />}
          />

          <Route
            path="/reports"
            element={<Reports />}
          />

          <Route
            path="/about"
            element={<About />}
          />
        </Routes>
      </AppShell>
    </BrowserRouter>
  );
}

export default App;