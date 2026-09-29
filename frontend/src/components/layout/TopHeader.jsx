import {
  MapPin,
  CalendarDays,
  User
} from "lucide-react";

function TopHeader() {

  return (

    <header className="top-header">

      <div className="header-brand">

        <div className="brand-cloud">
          ☁
        </div>

        <div>

          <h1>MEGHOVA</h1>

          <p>AI Rainfall Intelligence</p>

        </div>

      </div>


      <div className="header-controls">

        <div className="header-location">

          <MapPin size={18} />

          <span>
            Mangalore, Karnataka
          </span>

          <span>⌄</span>

        </div>


        <div className="header-date">

          <CalendarDays size={18} />

          <span>
            26 Sep 2026
          </span>

          <span>⌄</span>

        </div>


        <div className="user-icon">

          <User size={20} />

        </div>

      </div>

    </header>

  );
}

export default TopHeader;