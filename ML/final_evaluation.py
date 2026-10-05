import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error


# ============================================================
# 1. LOAD 2025 UNSEEN TEST RESULTS
# ============================================================

df = pd.read_csv("meghova_time_based_test_results.csv")

df["VT"] = pd.to_datetime(df["VT"])


# ============================================================
# 2. COLUMN NAMES
# ============================================================

actual = df["OBS_RAINFALL"]

nwp = df["TP_850"]

meghova = df["CORRECTED_RAINFALL"]


# ============================================================
# 3. ROW-BY-ROW ERRORS
# ============================================================

df["NWP_ERROR"] = nwp - actual

df["MEGHOVA_ERROR"] = meghova - actual

df["NWP_ABS_ERROR"] = abs(df["NWP_ERROR"])

df["MEGHOVA_ABS_ERROR"] = abs(df["MEGHOVA_ERROR"])


# ============================================================
# 4. RMSE
# ============================================================

nwp_rmse = np.sqrt(mean_squared_error(actual, nwp))

meghova_rmse = np.sqrt(mean_squared_error(actual, meghova))


# ============================================================
# 5. MAE
# ============================================================

nwp_mae = mean_absolute_error(actual, nwp)

meghova_mae = mean_absolute_error(actual, meghova)


# ============================================================
# 6. BIAS
# ============================================================

nwp_bias = np.mean(nwp - actual)

meghova_bias = np.mean(meghova - actual)


# ============================================================
# 7. RMSE IMPROVEMENT
# ============================================================

rmse_reduction = nwp_rmse - meghova_rmse

rmse_improvement = (
    (nwp_rmse - meghova_rmse) / nwp_rmse
) * 100


# ============================================================
# 8. PRINT OVERALL RESULTS
# ============================================================

print("\n==========================================")
print("       MEGHOVA FINAL EVALUATION")
print("==========================================")

print(f"\nTest samples: {len(df)}")

print("\nRMSE")
print(f"NWP      : {nwp_rmse:.4f}")
print(f"MEGHOVA  : {meghova_rmse:.4f}")

print("\nMAE")
print(f"NWP      : {nwp_mae:.4f}")
print(f"MEGHOVA  : {meghova_mae:.4f}")

print("\nBIAS")
print(f"NWP      : {nwp_bias:.4f}")
print(f"MEGHOVA  : {meghova_bias:.4f}")

print("\nRMSE REDUCTION")
print(f"Absolute reduction : {rmse_reduction:.4f}")
print(f"Improvement        : {rmse_improvement:.2f}%")


# ============================================================
# 9. RAINFALL EVENT METRICS
# ============================================================

def event_metrics(observed, predicted, threshold):

    obs_event = observed >= threshold
    pred_event = predicted >= threshold

    hits = np.sum(obs_event & pred_event)

    misses = np.sum(obs_event & ~pred_event)

    false_alarms = np.sum(~obs_event & pred_event)

    correct_negatives = np.sum(~obs_event & ~pred_event)

    # POD
    if hits + misses > 0:
        pod = hits / (hits + misses)
    else:
        pod = np.nan

    # FAR
    if hits + false_alarms > 0:
        far = false_alarms / (hits + false_alarms)
    else:
        far = np.nan

    # CSI
    if hits + misses + false_alarms > 0:
        csi = hits / (hits + misses + false_alarms)
    else:
        csi = np.nan

    # ETS
    total = hits + misses + false_alarms + correct_negatives

    random_hits = (
        (hits + misses) *
        (hits + false_alarms)
    ) / total if total > 0 else 0

    if (
        hits + misses + false_alarms - random_hits
    ) > 0:

        ets = (
            hits - random_hits
        ) / (
            hits + misses + false_alarms - random_hits
        )

    else:
        ets = np.nan

    return hits, misses, false_alarms, pod, far, csi, ets


# ============================================================
# 10. CALCULATE EVENT METRICS
# ============================================================

thresholds = [1, 5, 10]

print("\n==========================================")
print("       RAINFALL EVENT VERIFICATION")
print("==========================================")


for threshold in thresholds:

    nwp_result = event_metrics(
        actual,
        nwp,
        threshold
    )

    meghova_result = event_metrics(
        actual,
        meghova,
        threshold
    )

    print(f"\nThreshold >= {threshold} mm")

    print("\nNWP")
    print(f"Hits          : {nwp_result[0]}")
    print(f"Misses        : {nwp_result[1]}")
    print(f"False Alarms  : {nwp_result[2]}")
    print(f"POD           : {nwp_result[3]:.4f}")
    print(f"FAR           : {nwp_result[4]:.4f}")
    print(f"CSI           : {nwp_result[5]:.4f}")
    print(f"ETS           : {nwp_result[6]:.4f}")

    print("\nMEGHOVA")
    print(f"Hits          : {meghova_result[0]}")
    print(f"Misses        : {meghova_result[1]}")
    print(f"False Alarms  : {meghova_result[2]}")
    print(f"POD           : {meghova_result[3]:.4f}")
    print(f"FAR           : {meghova_result[4]:.4f}")
    print(f"CSI           : {meghova_result[5]:.4f}")
    print(f"ETS           : {meghova_result[6]:.4f}")


# ============================================================
# 11. SAVE ROW-BY-ROW COMPARISON
# ============================================================

comparison_columns = [
    "LAT",
    "LON",
    "VT",
    "WEATHER_REGIME",
    "PREDICTED_REGIME",
    "TP_850",
    "OBS_RAINFALL",
    "CORRECTED_RAINFALL",
    "NWP_ERROR",
    "MEGHOVA_ERROR",
    "NWP_ABS_ERROR",
    "MEGHOVA_ABS_ERROR"
]

available_columns = [
    col for col in comparison_columns
    if col in df.columns
]

comparison = df[available_columns]

comparison.to_csv(
    "meghova_nwp_vs_actual_vs_model.csv",
    index=False
)

print("\n==========================================")
print("Comparison saved:")
print("meghova_nwp_vs_actual_vs_model.csv")
print("==========================================")
