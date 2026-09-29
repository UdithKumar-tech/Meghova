import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import mean_squared_error


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("data/meghova_training_data.csv")

df["VT"] = pd.to_datetime(df["VT"])
df["MONTH"] = df["VT"].dt.month


# ============================================================
# 2. CONVERT NUMERICAL COLUMNS
# ============================================================

numeric_features = [
    "LAT", "LON",

    "GH_850", "T_850", "RH_850",
    "U_850", "V_850", "TP_850", "CAPE_850",

    "GH_500", "T_500", "RH_500",
    "U_500", "V_500", "TP_500", "CAPE_500",

    "OBS_RAINFALL"
]

for column in numeric_features:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


df = df.dropna(
    subset=numeric_features
).reset_index(drop=True)


# ============================================================
# 3. USE THE SAME TEST SPLIT AS OUR CLASSIFIER
# ============================================================

from sklearn.model_selection import train_test_split

train_df, test_df = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["WEATHER_REGIME"]
)


# ============================================================
# 4. LOAD TRAINED CLASSIFIER
# ============================================================

classifier = joblib.load("regime_classifier.pkl")
encoder = joblib.load("regime_label_encoder.pkl")


# ============================================================
# 5. LOAD FIVE TRAINED EXPERTS
# ============================================================

experts = {
    "ACTIVE": joblib.load("experts/active_expert.pkl"),
    "BREAK": joblib.load("experts/break_expert.pkl"),
    "NORMAL": joblib.load("experts/normal_expert.pkl"),
    "DEPRESSION": joblib.load("experts/depression_expert.pkl"),
    "COASTAL_OROGRAPHIC": joblib.load(
        "experts/coastal_orographic_expert.pkl"
    )
}


# ============================================================
# 6. CLASSIFIER FEATURES
# ============================================================

classifier_features = [
    "LAT", "LON", "MONTH",

    "GH_850", "T_850", "RH_850",
    "U_850", "V_850", "TP_850", "CAPE_850",

    "GH_500", "T_500", "RH_500",
    "U_500", "V_500", "TP_500", "CAPE_500"
]


# ============================================================
# 7. EXPERT FEATURES
# ============================================================

expert_features = [
    "LAT", "LON",

    "GH_850", "T_850", "RH_850",
    "U_850", "V_850", "TP_850", "CAPE_850",

    "GH_500", "T_500", "RH_500",
    "U_500", "V_500", "TP_500", "CAPE_500"
]


# ============================================================
# 8. SELECT TEST DATA
# ============================================================

X_test = test_df[classifier_features].astype(float)


# ============================================================
# 9. CLASSIFY REGIME
# ============================================================

predicted_numbers = classifier.predict(X_test)

test_df["PREDICTED_REGIME"] = encoder.inverse_transform(
    predicted_numbers.astype(int)
)


# ============================================================
# 10. APPLY CORRECT EXPERT
# ============================================================

test_df["PREDICTED_CORRECTION"] = 0.0


for regime in experts:

    mask = test_df["PREDICTED_REGIME"] == regime

    if mask.sum() == 0:
        continue

    X_expert = test_df.loc[
        mask,
        expert_features
    ].astype(float)

    corrections = experts[regime].predict(X_expert)

    test_df.loc[
        mask,
        "PREDICTED_CORRECTION"
    ] = corrections


# ============================================================
# 11. CALCULATE CORRECTED RAINFALL
# ============================================================

test_df["CORRECTED_RAINFALL"] = (
    test_df["TP_850"] +
    test_df["PREDICTED_CORRECTION"]
)

# Rainfall cannot be negative
test_df["CORRECTED_RAINFALL"] = (
    test_df["CORRECTED_RAINFALL"].clip(lower=0)
)


# ============================================================
# 12. CALCULATE RAW NWP RMSE
# ============================================================

observed = test_df["OBS_RAINFALL"]

raw_nwp = test_df["TP_850"]

corrected = test_df["CORRECTED_RAINFALL"]


raw_rmse = np.sqrt(
    mean_squared_error(
        observed,
        raw_nwp
    )
)


# ============================================================
# 13. CALCULATE CORRECTED RMSE
# ============================================================

corrected_rmse = np.sqrt(
    mean_squared_error(
        observed,
        corrected
    )
)


# ============================================================
# 14. DISPLAY RESULTS
# ============================================================

print("\n")
print("=" * 60)
print("MEGHOVA BIAS CORRECTION EVALUATION")
print("=" * 60)

print("\nTest samples:", len(test_df))

print("\nRaw NWP RMSE:")
print(round(raw_rmse, 4))

print("\nMEGHOVA Corrected RMSE:")
print(round(corrected_rmse, 4))


# ============================================================
# 15. CALCULATE RMSE IMPROVEMENT
# ============================================================

improvement = raw_rmse - corrected_rmse

print("\nRMSE Change:")
print(round(improvement, 4))

if improvement > 0:
    print("RMSE decreased after correction.")
else:
    print("RMSE did not decrease after correction.")


# ============================================================
# 16. SHOW REGIME DISTRIBUTION
# ============================================================

print("\n")
print("=" * 60)
print("PREDICTED REGIME DISTRIBUTION ON TEST DATA")
print("=" * 60)

print(
    test_df["PREDICTED_REGIME"].value_counts()
)


# ============================================================
# 17. SHOW SAMPLE PREDICTIONS
# ============================================================

print("\n")
print("=" * 90)
print("SAMPLE TEST PREDICTIONS")
print("=" * 90)

print(
    test_df[
        [
            "LAT",
            "LON",
            "VT",
            "TP_850",
            "PREDICTED_REGIME",
            "PREDICTED_CORRECTION",
            "CORRECTED_RAINFALL",
            "OBS_RAINFALL"
        ]
    ].head(20).to_string(index=False)
)


# ============================================================
# 18. SAVE TEST RESULTS
# ============================================================

test_df.to_csv(
    "meghova_test_results.csv",
    index=False
)

print("\nSaved:")
print("meghova_test_results.csv")