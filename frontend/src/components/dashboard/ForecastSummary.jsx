import { CloudRain } from "lucide-react";
import Card from "../common/Card";

export default function ForecastSummary({ result }) {
  if (!result) return <Card title="Forecast Summary"><div className="empty-state"><div className="empty-state-icon"><CloudRain size={20}/></div><h3>No live forecast yet</h3><p>Open Forecast and run the real ML pipeline. The result will appear here.</p></div></Card>;
  const delta = result.corrected_rainfall_mm - result.nwp_rainfall_mm;
  return <Card title="Forecast Summary">
    <div className="summary-location"><CloudRain size={35}/><div><strong>{result.latitude.toFixed(3)}°N, {result.longitude.toFixed(3)}°E</strong><p>{result.valid_time ? new Date(result.valid_time).toLocaleString("en-IN") : "Selected NWP time"}</p></div></div>
    <div className="summary-main">
      <div><span>NWP Forecast</span><strong>{result.nwp_rainfall_mm.toFixed(1)} mm</strong></div>
      <div><span>Corrected Forecast</span><strong>{result.corrected_rainfall_mm.toFixed(1)} mm</strong><small>{delta >= 0 ? "↑" : "↓"} {Math.abs(delta).toFixed(1)} mm</small></div>
      <div><span>Predicted Regime</span><strong>{result.predicted_regime.replaceAll("_", " ")}</strong></div>
    </div>
    <div className="summary-bottom"><div><span>Rainfall category</span><strong>{result.rainfall_category}</strong><div className="progress"><div style={{width: `${Math.min(100, result.corrected_rainfall_mm / 2)}%`}} /></div></div><div><span>Model correction</span><strong>{result.predicted_correction_mm >= 0 ? "+" : ""}{result.predicted_correction_mm.toFixed(2)} mm</strong></div></div>
  </Card>;
}
