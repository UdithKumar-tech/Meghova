import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error

# -----------------------------
# 1. Load files
# -----------------------------

pred = pd.read_csv("meghova_future_predictions.csv")

obs = pd.read_csv(
    "data/karnataka_nwp_forecast_2026 (1).csv"
)

# -----------------------------
# 2. Convert dates
# -----------------------------

pred["VT"] = pd.to_datetime(pred["VT"])
obs["VT"] = pd.to_datetime(obs["VT"])

# -----------------------------
# 3. Keep 850 hPa observations
# -----------------------------

obs_850 = obs[obs["PL"] == 850].copy()

# Keep only columns needed
obs_850 = obs_850[
    ["VT", "LAT", "LON", "OBS_RAINFALL"]
]

# -----------------------------
# 4. Match predictions
#    with observations
# -----------------------------

result = pred.merge(
    obs_850,
    on=["VT", "LAT", "LON"],
    how="inner"
)

# -----------------------------
# 5. Display comparison
# -----------------------------

print("\n2026 NWP vs MEGHOVA vs ACTUAL")
print("=" * 60)

print(
    result[
        [
            "VT",
            "LAT",
            "LON",
            "OBS_RAINFALL",
            "TP_850",
            "MEGHOVA_PREDICTED_RAINFALL"
        ]
    ].to_string(index=False)
)

# -----------------------------
# 6. Calculate RMSE
# -----------------------------

nwp_rmse = np.sqrt(
    mean_squared_error(
        result["OBS_RAINFALL"],
        result["TP_850"]
    )
)

meghova_rmse = np.sqrt(
    mean_squared_error(
        result["OBS_RAINFALL"],
        result["MEGHOVA_PREDICTED_RAINFALL"]
    )
)

# -----------------------------
# 7. Calculate MAE
# -----------------------------

nwp_mae = mean_absolute_error(
    result["OBS_RAINFALL"],
    result["TP_850"]
)

meghova_mae = mean_absolute_error(
    result["OBS_RAINFALL"],
    result["MEGHOVA_PREDICTED_RAINFALL"]
)

# -----------------------------
# 8. RMSE improvement
# -----------------------------

rmse_improvement = (
    (nwp_rmse - meghova_rmse)
    / nwp_rmse
) * 100

# -----------------------------
# 9. Print results
# -----------------------------

print("\n")
print("=" * 60)
print("2026 EVALUATION RESULTS")
print("=" * 60)

print(f"NWP RMSE      : {nwp_rmse:.4f} mm")
print(f"MEGHOVA RMSE  : {meghova_rmse:.4f} mm")

print()

print(f"NWP MAE       : {nwp_mae:.4f} mm")
print(f"MEGHOVA MAE   : {meghova_mae:.4f} mm")

print()

print(
    f"RMSE change   : {rmse_improvement:.2f}%"
)

print()

if meghova_rmse < nwp_rmse:
    print("MEGHOVA has lower RMSE than NWP.")
else:
    print("NWP has lower RMSE than MEGHOVA.")

# -----------------------------
# 10. Save comparison
# -----------------------------

result.to_csv(
    "meghova_2026_evaluation.csv",
    index=False
)

print()
print("Comparison saved to:")
print("meghova_2026_evaluation.csv")
