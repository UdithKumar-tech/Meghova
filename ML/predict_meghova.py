import pandas as pd
import joblib


# ============================================================
# 1. LOAD REGIME CLASSIFIER
# ============================================================

classifier = joblib.load("regime_classifier.pkl")
encoder = joblib.load("regime_label_encoder.pkl")


# ============================================================
# 2. LOAD REGIME-SPECIFIC EXPERTS
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
# 3. LOAD DATA
# ============================================================

df = pd.read_csv("data/meghova_training_data.csv")

df["VT"] = pd.to_datetime(df["VT"])

# Month is needed by the classifier
df["MONTH"] = df["VT"].dt.month


# ============================================================
# 4. DEFINE NUMERICAL FEATURES
# ============================================================

numeric_features = [
    "LAT",
    "LON",

    "GH_850",
    "T_850",
    "RH_850",
    "U_850",
    "V_850",
    "TP_850",
    "CAPE_850",

    "GH_500",
    "T_500",
    "RH_500",
    "U_500",
    "V_500",
    "TP_500",
    "CAPE_500",

    "OBS_RAINFALL"
]


# ============================================================
# 5. FORCE ALL NUMERICAL COLUMNS TO FLOAT
# ============================================================

for column in numeric_features:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# Remove rows with invalid values
df = df.dropna(
    subset=numeric_features
).reset_index(drop=True)


# ============================================================
# 6. CLASSIFIER FEATURES
# ============================================================

classifier_features = [
    "LAT",
    "LON",
    "MONTH",

    "GH_850",
    "T_850",
    "RH_850",
    "U_850",
    "V_850",
    "TP_850",
    "CAPE_850",

    "GH_500",
    "T_500",
    "RH_500",
    "U_500",
    "V_500",
    "TP_500",
    "CAPE_500"
]


# ============================================================
# 7. EXPERT FEATURES
# ============================================================

expert_features = [
    "LAT",
    "LON",

    "GH_850",
    "T_850",
    "RH_850",
    "U_850",
    "V_850",
    "TP_850",
    "CAPE_850",

    "GH_500",
    "T_500",
    "RH_500",
    "U_500",
    "V_500",
    "TP_500",
    "CAPE_500"
]


# ============================================================
# 8. MAKE SURE CLASSIFIER INPUT IS FLOAT
# ============================================================

X_classify = df[classifier_features].astype(float)


# ============================================================
# 9. CLASSIFY WEATHER REGIME
# ============================================================

predicted_numbers = classifier.predict(X_classify)

df["PREDICTED_REGIME"] = encoder.inverse_transform(
    predicted_numbers.astype(int)
)


# ============================================================
# 10. PREDICT RAINFALL CORRECTION
# ============================================================

predicted_corrections = []

for regime, group in df.groupby("PREDICTED_REGIME", sort=False):

    print(
        "Using expert:",
        regime,
        "| Samples:",
        len(group)
    )

    # Select correct expert
    expert = experts[regime]

    # Get rows belonging to this predicted regime
    X_expert = group[expert_features].copy()

    # Explicitly convert everything to float
    X_expert = X_expert.astype(float)

    # Predict correction
    corrections = expert.predict(X_expert)

    # Store results using original row positions
    for value in corrections:
        predicted_corrections.append(value)


# ============================================================
# 11. RE-CREATE CORRECTIONS IN ORIGINAL ORDER
# ============================================================

# The grouped predictions above may not be in original row order,
# so create them again safely using each regime's row indices.

df["PREDICTED_CORRECTION"] = 0.0

for regime in experts:

    mask = df["PREDICTED_REGIME"] == regime

    X_expert = df.loc[
        mask,
        expert_features
    ].astype(float)

    df.loc[
        mask,
        "PREDICTED_CORRECTION"
    ] = experts[regime].predict(X_expert)


# ============================================================
# 12. CALCULATE CORRECTED RAINFALL
# ============================================================

df["CORRECTED_RAINFALL"] = (
    df["TP_850"] +
    df["PREDICTED_CORRECTION"]
)


# Rainfall cannot be negative
df["CORRECTED_RAINFALL"] = (
    df["CORRECTED_RAINFALL"].clip(lower=0)
)


# ============================================================
# 13. DISPLAY RESULTS
# ============================================================

print("\n")
print("=" * 90)
print("MEGHOVA PREDICTION RESULTS")
print("=" * 90)

print(
    df[
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
# 14. SHOW PREDICTED REGIME COUNTS
# ============================================================

print("\n")
print("=" * 50)
print("PREDICTED REGIME DISTRIBUTION")
print("=" * 50)

print(
    df["PREDICTED_REGIME"].value_counts()
)


# ============================================================
# 15. SAVE RESULTS
# ============================================================

df.to_csv(
    "meghova_predictions.csv",
    index=False
)


print("\n")
print("=" * 50)
print("PIPELINE COMPLETED")
print("=" * 50)

print("Saved: meghova_predictions.csv")