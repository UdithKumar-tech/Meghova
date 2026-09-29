function MetricCard({
  title,
  value,
  unit,
  subtitle,
  icon,
  variant = "blue"
}) {

  return (

    <div className={`metric-card ${variant}`}>

      <div className="metric-icon">
        {icon}
      </div>

      <div className="metric-content">

        <div className="metric-title">
          {title}
        </div>

        <div className="metric-value">

          {value}

          {unit && (
            <span>{unit}</span>
          )}

        </div>

        <div className="metric-subtitle">
          {subtitle}
        </div>

      </div>

    </div>

  );
}

export default MetricCard;