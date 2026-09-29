import {
  Cloud,
  CloudSun,
  Droplets,
  Umbrella
} from "lucide-react";

import MetricCard from "../common/MetricCard";

function KPIGrid() {

  return (

    <section className="kpi-grid">

      <MetricCard
        title="NWP Forecast"
        value="80"
        unit=" mm"
        subtitle="for selected area"
        icon={<Cloud size={27} />}
        variant="blue"
      />

      <MetricCard
        title="Weather Regime"
        value="Active Monsoon"
        subtitle="High rainfall probability"
        icon={<CloudSun size={27} />}
        variant="green"
      />

      <MetricCard
        title="Corrected Forecast"
        value="102"
        unit=" mm"
        subtitle="↑ 22 mm vs. NWP"
        icon={<Droplets size={27} />}
        variant="purple"
      />

      <MetricCard
        title="Heavy Rain Probability"
        value="81%"
        subtitle="> 50 mm"
        icon={<Umbrella size={27} />}
        variant="pink"
      />

    </section>

  );
}

export default KPIGrid;