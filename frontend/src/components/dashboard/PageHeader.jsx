import {
  MapPin,
  CalendarDays
} from "lucide-react";

function PageHeader() {

  return (

    <section className="page-header">

      <div>

        <div className="eyebrow">
          AI-POWERED WEATHER INTELLIGENCE
        </div>

        <h1>
          Regime-Aware Rainfall Forecast
        </h1>

        <p>
          Using weather-regime information to
          correct NWP forecasts and provide
          accurate rainfall predictions.
        </p>

      </div>


      <div className="page-actions">

        <button className="select-button">

          <MapPin size={17} />

          Mangalore, Karnataka

          <span>⌄</span>

        </button>


        <button className="select-button">

          <CalendarDays size={17} />

          26 Sep 2026

          <span>⌄</span>

        </button>


        <button className="primary-button">

          View Forecast

        </button>

      </div>

    </section>

  );
}

export default PageHeader;
