import {
  Home,
  Map,
  CloudRain,
  BarChart3,
  FileText,
  Info
} from "lucide-react";

import { NavLink } from "react-router-dom";

const navigation = [
  {
    name: "Overview",
    path: "/",
    icon: Home
  },
  {
    name: "Rainfall Map",
    path: "/rainfall-map",
    icon: Map
  },
  {
    name: "Forecast",
    path: "/forecast",
    icon: CloudRain
  },
  {
    name: "Model Performance",
    path: "/model-performance",
    icon: BarChart3
  },
  {
    name: "Reports",
    path: "/reports",
    icon: FileText
  },
  {
    name: "About",
    path: "/about",
    icon: Info
  }
];

function Sidebar() {

  return (

    <aside className="sidebar">

      <div className="sidebar-logo">

        <div className="logo-icon">
          ☁
        </div>

        <div>
          <h1>MEGHOVA</h1>

          <p>
            AI Rainfall Intelligence
          </p>
        </div>

      </div>

      <nav className="sidebar-nav">

        {navigation.map((item) => {

          const Icon = item.icon;

          return (

            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >

              <Icon size={20} />

              <span>
                {item.name}
              </span>

            </NavLink>

          );

        })}

      </nav>

      <div className="sidebar-footer">

        <div className="footer-leaf">
          🌱
        </div>

        <p>
          Smarter forecasts.<br />
          Safer communities.
        </p>

      </div>

    </aside>

  );
}

export default Sidebar;