import { CalendarDays, MapPin, RefreshCw } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function PageHeader() {
  const [location, setLocation] = useState("Karnataka");
  const [date, setDate] = useState("2026-06-02");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const locations = ["Karnataka", "Mangalore", "Udupi", "Mysuru", "Bengaluru", "Hubballi"];
  const formatted = new Date(`${date}T00:00:00`).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });

  const viewForecast = () => {
    setLoading(true);
    setTimeout(() => { setLoading(false); navigate("/forecast"); }, 250);
  };

  return (
    <section className="page-header">
      <div>
        <div className="eyebrow">AI-POWERED WEATHER INTELLIGENCE</div>
        <h1>Regime-Aware Rainfall Forecast</h1>
        <p>MEGHOVA combines NWP atmospheric variables with regime-specific XGBoost correction models to improve rainfall guidance.</p>
      </div>
      <div className="page-actions">
        <label className="select-button"><MapPin size={17} /><select value={location} onChange={e => setLocation(e.target.value)}>{locations.map(x => <option key={x}>{x}</option>)}</select></label>
        <label className="select-button"><CalendarDays size={17} /><input type="date" value={date} onChange={e => setDate(e.target.value)} /><span>{formatted}</span></label>
        <button className="primary-button" onClick={viewForecast}><RefreshCw size={16} className={loading ? "spin" : ""} /> View Forecast</button>
      </div>
    </section>
  );
}
