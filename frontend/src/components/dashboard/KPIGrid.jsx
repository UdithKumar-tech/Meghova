import { CloudRain, CloudSun, Droplets, Gauge } from "lucide-react";
import MetricCard from "../common/MetricCard";

export default function KPIGrid({ summary }) {
  const r = summary?.corrected_rainfall_mm ?? 0;
  const nwp = summary?.nwp_rainfall_mm ?? 0;
  const correction = summary?.predicted_correction_mm ?? 0;
  const regime = summary?.predicted_regime ?? "—";
  return <section className="kpi-grid">
    <MetricCard title="NWP Rainfall" value={nwp.toFixed(1)} unit=" mm" subtitle="Raw numerical forecast" icon={<CloudRain size={26}/>} variant="blue" />
    <MetricCard title="Weather Regime" value={regime.replaceAll("_", " ")} subtitle="ML classified regime" icon={<CloudSun size={26}/>} variant="green" />
    <MetricCard title="MEGHOVA Corrected" value={r.toFixed(1)} unit=" mm" subtitle={`${correction >= 0 ? "+" : ""}${correction.toFixed(1)} mm correction`} icon={<Droplets size={26}/>} variant="purple" />
    <MetricCard title="Rainfall Category" value={summary?.rainfall_category || "—"} subtitle="Based on corrected amount" icon={<Gauge size={26}/>} variant="pink" />
  </section>;
}
