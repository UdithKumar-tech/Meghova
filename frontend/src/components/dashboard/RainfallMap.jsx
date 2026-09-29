import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

import Card from "../common/Card";

const rainfallPoints = [
  {
    lat: 12.91,
    lon: 74.85,
    rainfall: 102,
    name: "Mangalore"
  },

  {
    lat: 13.05,
    lon: 74.95,
    rainfall: 75,
    name: "Udupi"
  },

  {
    lat: 12.60,
    lon: 75.00,
    rainfall: 130,
    name: "Kasargod"
  },

  {
    lat: 13.30,
    lon: 75.70,
    rainfall: 50,
    name: "Chikkamagaluru"
  }
];

function rainfallColor(value) {

  if (value >= 150) return "#d91e5b";

  if (value >= 100) return "#ff4b2b";

  if (value >= 75) return "#ffb000";

  if (value >= 50) return "#d6e636";

  if (value >= 25) return "#25bfa7";

  return "#198bd1";
}

function RainfallMap() {

  return (

    <Card title="Rainfall Forecast Map">

      <div className="map-tabs">

        <button>NWP</button>

        <button className="active">
          Corrected
        </button>

        <button>Observed</button>

      </div>

      <div className="map-container">

        <MapContainer
          center={[12.8, 75.1]}
          zoom={8}
          style={{
            height: "100%",
            width: "100%"
          }}
        >

          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {rainfallPoints.map((point) => (

            <CircleMarker
              key={point.name}
              center={[
                point.lat,
                point.lon
              ]}
              radius={35}
              pathOptions={{
                color: rainfallColor(point.rainfall),
                fillColor:
                  rainfallColor(point.rainfall),
                fillOpacity: 0.55,
                weight: 0
              }}
            >

              <Popup>
                <strong>
                  {point.name}
                </strong>

                <br />

                Rainfall:
                {" "}
                {point.rainfall}
                {" "}
                mm

              </Popup>

            </CircleMarker>

          ))}

        </MapContainer>

      </div>

    </Card>

  );
}

export default RainfallMap;