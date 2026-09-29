import PageHeader
  from "../components/dashboard/PageHeader";

import KPIGrid
  from "../components/dashboard/KPIGrid";

import RainfallMap
  from "../components/dashboard/RainfallMap";

import ForecastSummary
  from "../components/dashboard/ForecastSummary";

import RainfallChart
  from "../components/dashboard/RainfallChart";

import RegimeDistribution
  from "../components/dashboard/RegimeDistribution";

import ModelPerformance
  from "../components/dashboard/ModelPerformance";


function Dashboard() {

  return (

    <div>

      <PageHeader />

      <KPIGrid />


      <div className="main-analysis-grid">

        <RainfallMap />

        <ForecastSummary />

      </div>


      <div className="bottom-analysis-grid">

        <RainfallChart />

        <RegimeDistribution />

        <ModelPerformance />

      </div>

    </div>

  );
}

export default Dashboard;