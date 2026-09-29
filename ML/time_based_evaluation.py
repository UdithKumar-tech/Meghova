import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    mean_squared_error
)
from xgboost import XGBClassifier, XGBRegressor


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv("data/meghova_training_data.csv")

df["VT"] = pd.to_datetime(df["VT"])
df["YEAR"] = df["VT"].dt.year
df["MONTH"] = df["VT"].dt.month

numeric_features = [
    "LAT", "LON",
    "GH_850", "T_850", "RH_850",
    "U_850", "V_850", "TP_850", "CAPE_850",
    "GH_500", "T_500", "RH_500",
    "U_500", "V_500", "TP_500", "CAPE_500",
    "OBS_RAINFALL"
]

for column in numeric_features:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.dropna(subset=numeric_features).reset_index(drop=True)

df["CORRECTION"] = df["OBS_RAINFALL"] - df["TP_850"]


# ============================================================
# FEATURES
# ============================================================

classifier_features = [
    "LAT", "LON", "MONTH",
    "GH_850", "T_850", "RH_850",
    "U_850", "V_850", "TP_850", "CAPE_850",
    "GH_500", "T_500", "RH_500",
    "U_500", "V_500", "TP_500", "CAPE_500"
]

expert_features = [
    "LAT", "LON",
    "GH_850", "T_850", "RH_850",
    "U_850", "V_850", "TP_850", "CAPE_850",
    "GH_500", "T_500", "RH_500",
    "U_500", "V_500", "TP_500", "CAPE_500"
]


# ============================================================
# TIME-BASED TRAIN / TEST SPLIT
# ============================================================

train_df = df[df["YEAR"] <= 2024].copy()
test_df = df[df["YEAR"] == 2025].copy()

train_df = train_df.reset_index(drop=True)
test_df = test_df.reset_index(drop=True)

print("\n")
print("=" * 70)
print("TIME-BASED LEAKAGE-FREE EVALUATION")
print("=" * 70)

print("\nTraining years: 2021-2024")
print("Testing year : 2025")

print("\nTraining samples:", len(train_df))
print("Testing samples :", len(test_df))


# ============================================================
# REGIME DISTRIBUTION
# ============================================================

print("\n")
print("=" * 70)
print("TRAINING REGIME DISTRIBUTION")
print("=" * 70)

print(train_df["WEATHER_REGIME"].value_counts())

print("\n")
print("=" * 70)
print("TESTING REGIME DISTRIBUTION")
print("=" * 70)

print(test_df["WEATHER_REGIME"].value_counts())


# ============================================================
# TRAIN REGIME CLASSIFIER
# ============================================================

print("\n")
print("=" * 70)
print("TRAINING REGIME CLASSIFIER")
print("=" * 70)

encoder = LabelEncoder()

y_train = encoder.fit_transform(
    train_df["WEATHER_REGIME"]
)

X_train_classifier = (
    train_df[classifier_features]
    .astype(float)
)

classifier = XGBClassifier(
    n_estimators=150,
    max_depth=3,
    learning_rate=0.05,
    objective="multi:softprob",
    num_class=len(encoder.classes_),
    eval_metric="mlogloss",
    random_state=42
)

classifier.fit(
    X_train_classifier,
    y_train
)


# ============================================================
# TEST REGIME CLASSIFIER
# ============================================================

X_test_classifier = (
    test_df[classifier_features]
    .astype(float)
)

predicted_numbers = classifier.predict(
    X_test_classifier
)

test_df["PREDICTED_REGIME"] = (
    encoder.inverse_transform(
        predicted_numbers.astype(int)
    )
)

classification_accuracy = accuracy_score(
    test_df["WEATHER_REGIME"],
    test_df["PREDICTED_REGIME"]
)

print("\nClassifier Accuracy:")
print(round(classification_accuracy, 4))

print("\nClassification Report:")

print(
    classification_report(
        test_df["WEATHER_REGIME"],
        test_df["PREDICTED_REGIME"],
        labels=encoder.classes_,
        zero_division=0
    )
)


# ============================================================
# TRAIN REGIME-SPECIFIC EXPERTS
# ============================================================

print("\n")
print("=" * 70)
print("TRAINING REGIME-SPECIFIC RAINFALL EXPERTS")
print("=" * 70)

regimes = [
    "ACTIVE",
    "BREAK",
    "NORMAL",
    "DEPRESSION",
    "COASTAL_OROGRAPHIC"
]

experts = {}

for regime in regimes:

    print("\nTraining:", regime)

    regime_train = train_df[
        train_df["WEATHER_REGIME"] == regime
    ]

    print(
        "Training samples:",
        len(regime_train)
    )

    X_regime = (
        regime_train[expert_features]
        .astype(float)
    )

    y_regime = (
        regime_train["CORRECTION"]
        .astype(float)
    )

    expert = XGBRegressor(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.05,
        objective="reg:squarederror",
        random_state=42
    )

    expert.fit(
        X_regime,
        y_regime
    )

    experts[regime] = expert


# ============================================================
# APPLY EXPERTS USING PREDICTED REGIME
# ============================================================

test_df["PREDICTED_CORRECTION"] = 0.0

print("\n")
print("=" * 70)
print("APPLYING REGIME-SPECIFIC EXPERTS")
print("=" * 70)

for regime in regimes:

    mask = (
        test_df["PREDICTED_REGIME"]
        == regime
    )

    if mask.sum() == 0:

        print(
            regime,
            "→ no test samples"
        )

        continue

    print(
        regime,
        "→",
        mask.sum(),
        "test samples"
    )

    X_expert = (
        test_df.loc[
            mask,
            expert_features
        ]
        .astype(float)
    )

    corrections = experts[
        regime
    ].predict(X_expert)

    test_df.loc[
        mask,
        "PREDICTED_CORRECTION"
    ] = corrections


# ============================================================
# CALCULATE CORRECTED RAINFALL
# ============================================================

test_df["CORRECTED_RAINFALL"] = (
    test_df["TP_850"]
    + test_df["PREDICTED_CORRECTION"]
)

test_df["CORRECTED_RAINFALL"] = (
    test_df["CORRECTED_RAINFALL"]
    .clip(lower=0)
)


# ============================================================
# RMSE
# ============================================================

observed = (
    test_df["OBS_RAINFALL"]
    .astype(float)
)

raw_nwp = (
    test_df["TP_850"]
    .astype(float)
)

corrected = (
    test_df["CORRECTED_RAINFALL"]
    .astype(float)
)

raw_rmse = np.sqrt(
    mean_squared_error(
        observed,
        raw_nwp
    )
)

meghova_rmse = np.sqrt(
    mean_squared_error(
        observed,
        corrected
    )
)

rmse_reduction = (
    raw_rmse
    - meghova_rmse
)

if raw_rmse != 0:

    improvement_percent = (
        rmse_reduction
        / raw_rmse
    ) * 100

else:

    improvement_percent = 0


# ============================================================
# FINAL RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("FINAL TIME-BASED MEGHOVA EVALUATION")
print("=" * 70)

print("\nRaw NWP RMSE:")
print(round(raw_rmse, 4))

print("\nMEGHOVA Corrected RMSE:")
print(round(meghova_rmse, 4))

print("\nRMSE Reduction:")
print(round(rmse_reduction, 4))

print("\nRMSE Improvement (%):")
print(round(improvement_percent, 2))


# ============================================================
# PREDICTED REGIME DISTRIBUTION
# ============================================================

print("\n")
print("=" * 70)
print("PREDICTED REGIME DISTRIBUTION")
print("=" * 70)

print(
    test_df["PREDICTED_REGIME"]
    .value_counts()
)


# ============================================================
# ACTUAL VS PREDICTED
# ============================================================

print("\n")
print("=" * 70)
print("ACTUAL VS PREDICTED REGIME")
print("=" * 70)

print(
    pd.crosstab(
        test_df["WEATHER_REGIME"],
        test_df["PREDICTED_REGIME"]
    )
)


# ============================================================
# SAMPLE RESULTS
# ============================================================

print("\n")
print("=" * 100)
print("2025 TEST RESULTS")
print("=" * 100)

print(
    test_df[
        [
            "LAT",
            "LON",
            "VT",
            "WEATHER_REGIME",
            "PREDICTED_REGIME",
            "TP_850",
            "PREDICTED_CORRECTION",
            "CORRECTED_RAINFALL",
            "OBS_RAINFALL"
        ]
    ]
    .head(20)
    .to_string(index=False)
)


# ============================================================
# SAVE RESULTS
# ============================================================

test_df.to_csv(
    "meghova_time_based_test_results.csv",
    index=False
)

print("\n")
print("Saved:")
print("meghova_time_based_test_results.csv")