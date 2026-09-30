import pandas as pd
import joblib

from xgboost import XGBRegressor


# 1. Load dataset
df = pd.read_csv("data/meghova_training_data.csv")


# 2. Create rainfall correction target
# Correction = Observed rainfall - NWP rainfall
df["CORRECTION"] = df["OBS_RAINFALL"] - df["TP_850"]


# 3. Features used by every expert
features = [
    "LAT", "LON",

    "GH_850", "T_850", "RH_850",
    "U_850", "V_850", "TP_850", "CAPE_850",

    "GH_500", "T_500", "RH_500",
    "U_500", "V_500", "TP_500", "CAPE_500"
]


# 4. Train one expert for each regime
regimes = [
    "ACTIVE",
    "BREAK",
    "NORMAL",
    "DEPRESSION",
    "COASTAL_OROGRAPHIC"
]


for regime in regimes:

    print("\nTraining expert for:", regime)

    # Select only data belonging to this regime
    regime_data = df[df["WEATHER_REGIME"] == regime]

    X = regime_data[features]
    y = regime_data["CORRECTION"]

    print("Training samples:", len(regime_data))

    # XGBoost regression expert
    model = XGBRegressor(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.05,
        objective="reg:squarederror",
        random_state=42
    )

    # Train
    model.fit(X, y)

    # Save expert
    filename = "experts/" + regime.lower() + "_expert.pkl"

    joblib.dump(model, filename)

    print("Saved:", filename)


print("\nAll regime experts trained successfully.")