import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";

import Card from "../common/Card";

const data = [
  {
    date: "26 Sep",
    observed: 25,
    nwp: 35,
    corrected: 42
  },
  {
    date: "27 Sep",
    observed: 40,
    nwp: 52,
    corrected: 70
  },
  {
    date: "28 Sep",
    observed: 62,
    nwp: 85,
    corrected: 140
  },
  {
    date: "29 Sep",
    observed: 55,
    nwp: 60,
    corrected: 95
  },
  {
    date: "30 Sep",
    observed: 38,
    nwp: 48,
    corrected: 60
  }
];

function RainfallChart() {

  return (

    <Card title="Rainfall Forecast (Time Series)">

      <div className="chart-container">

        <ResponsiveContainer
          width="100%"
          height="100%"
        >

          <ComposedChart data={data}>

            <CartesianGrid
              strokeDasharray="3 3"
            />

            <XAxis
              dataKey="date"
            />

            <YAxis
              label={{
                value: "Rainfall (mm)",
                angle: -90,
                position: "insideLeft"
              }}
            />

            <Tooltip />

            <Legend />

            <Bar
              dataKey="observed"
              name="Observed"
              fill="#1976D2"
              barSize={20}
            />

            <Line
              type="monotone"
              dataKey="nwp"
              name="NWP"
              stroke="#F5A623"
              strokeWidth={2}
              dot={{ r: 3 }}
            />

            <Line
              type="monotone"
              dataKey="corrected"
              name="Corrected"
              stroke="#10B981"
              strokeWidth={2}
              dot={{ r: 3 }}
            />

          </ComposedChart>

        </ResponsiveContainer>

      </div>

    </Card>

  );
}

export default RainfallChart;