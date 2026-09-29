import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend
} from "recharts";

import Card from "../common/Card";

const data = [
  {
    name: "Active Monsoon",
    value: 68
  },
  {
    name: "Break Monsoon",
    value: 18
  },
  {
    name: "Depression",
    value: 9
  },
  {
    name: "Others",
    value: 5
  }
];

const COLORS = [
  "#1976D2",
  "#F5A623",
  "#10B981",
  "#8B5CF6"
];

function RegimeDistribution() {

  return (

    <Card title="Weather Regime Distribution">

      <div className="regime-chart">

        <ResponsiveContainer
          width="100%"
          height={250}
        >

          <PieChart>

            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              innerRadius={55}
              outerRadius={82}
            >

              {data.map(
                (_, index) => (
                  <Cell
                    key={index}
                    fill={COLORS[index]}
                  />
                )
              )}

            </Pie>

            <Legend />

          </PieChart>

        </ResponsiveContainer>

      </div>

    </Card>

  );
}

export default RegimeDistribution;