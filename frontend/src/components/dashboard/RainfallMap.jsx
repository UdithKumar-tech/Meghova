import { useEffect, useState } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import Card from "../common/Card";
import { getMapForecast } from "../../services/Api";

const color = v => v >= 150 ? "#d91e5b" : v >= 100 ? "#ff4b2b" : v >= 75 ? "#ffb000" : v >= 50 ? "#d6e636" : v >= 25 ? "#25bfa7" : "#198bd1";
function FitMap({ points }) { const map = useMap(); useEffect(() => { if (points.length) map.fitBounds(points.map(p => [p.lat,p.lon]), {padding:[20,20]}); }, [points,map]); return null; }

export default function RainfallMap({ compact = true }) {
  const [points, setPoints] = useState([]); const [error,setError]=useState("");
  useEffect(() => { getMapForecast().then(d=>setPoints(d.locations||[])).catch(e=>setError(e?.response?.data?.detail||"Could not load map forecast.")); }, []);
  return <Card title="Rainfall Forecast Map">
    {error && <div className="api-warning">{error}</div>}
    <div className={`map-container ${compact ? "" : "large-map"}`}>
      <MapContainer center={[15.3,75.7]} zoom={7} scrollWheelZoom style={{height:"100%",width:"100%"}}>
        <TileLayer attribution="&copy; OpenStreetMap contributors" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <FitMap points={points}/>
        {points.map((p,i)=><CircleMarker key={`${p.lat}-${p.lon}-${i}`} center={[p.lat,p.lon]} radius={compact?18:24} pathOptions={{color:color(p.rainfall),fillColor:color(p.rainfall),fillOpacity:.65,weight:2}}><Popup><strong>{p.lat.toFixed(3)}°, {p.lon.toFixed(3)}°</strong><br/>Corrected rainfall: {p.rainfall.toFixed(2)} mm<br/>NWP: {p.nwp_rainfall.toFixed(2)} mm<br/>Regime: {p.regime.replaceAll("_"," ")}<br/>Category: {p.category}</Popup></CircleMarker>)}
      </MapContainer>
    </div>
    <div className="legend-items"><span className="legend-item"><i className="legend-dot light"/>25–50</span><span className="legend-item"><i className="legend-dot moderate"/>50–75</span><span className="legend-item"><i className="legend-dot heavy"/>75–100</span><span className="legend-item"><i className="legend-dot very-heavy"/>100–150</span><span className="legend-item"><i className="legend-dot extreme"/>&gt;150 mm</span></div>
  </Card>;
}
