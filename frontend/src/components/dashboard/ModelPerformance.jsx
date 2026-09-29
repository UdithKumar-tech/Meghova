const metrics = [
  ["RMSE (mm)", "42.3", "34.1", "19.4%"],
  ["CSI", "0.41", "0.55", "34.1%"],
  ["POD", "0.62", "0.74", "19.4%"],
  ["FAR", "0.32", "0.22", "31.3%"],
  ["ETS", "0.38", "0.52", "36.8%"],
  ["FSS", "0.61", "0.74", "21.3%"]
];

import Card from "../common/Card";

function ModelPerformance() {

  return (

    <Card title="Model Performance (Test Set)">

      <div className="performance-tabs">

        <button className="active">
          Overall
        </button>

        <button>
          By Regime
        </button>

        <button>
          By Rainfall Intensity
        </button>

      </div>


      <table className="performance-table">

        <thead>

          <tr>

            <th>Metric</th>

            <th>Raw NWP</th>

            <th>Corrected</th>

            <th>Improvement</th>

          </tr>

        </thead>


        <tbody>

          {metrics.map(
            (metric) => (

              <tr key={metric[0]}>

                <td>{metric[0]}</td>

                <td>{metric[1]}</td>

                <td>{metric[2]}</td>

                <td>
                  ↑ {metric[3]}
                </td>

              </tr>

            )
          )}

        </tbody>

      </table>

    </Card>

  );
}

export default ModelPerformance;