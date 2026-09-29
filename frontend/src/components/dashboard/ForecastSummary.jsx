import {
  CloudRain,
  Umbrella,
  CloudLightning
} from "lucide-react";

import Card from "../common/Card";

function ForecastSummary() {

  return (

    <Card title="Forecast Summary">

      <div className="summary-location">

        <CloudRain size={35} />

        <div>

          <strong>
            Mangalore, Karnataka
          </strong>

          <p>
            26 Sep 2026 • 08:00 AM (IST)
          </p>

        </div>

      </div>


      <div className="summary-main">

        <div>

          <span>NWP Forecast</span>

          <strong>80 mm</strong>

        </div>


        <div>

          <span>Corrected Forecast</span>

          <strong>102 mm</strong>

          <small>
            ↑ 22 mm
          </small>

        </div>


        <div>

          <span>Regime</span>

          <strong>
            Active Monsoon
          </strong>

        </div>

      </div>


      <div className="summary-bottom">

        <div>

          <span>
            Heavy Rain Probability
          </span>

          <strong>
            81%
          </strong>

          <div className="progress">

            <div
              style={{
                width: "81%"
              }}
            />

          </div>

        </div>


        <div>

          <span>
            Likely Rainfall Range
          </span>

          <strong>
            50 – 150 mm
          </strong>

        </div>

      </div>

    </Card>

  );
}

export default ForecastSummary;