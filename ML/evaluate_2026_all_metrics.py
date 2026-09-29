import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv("meghova_2026_evaluation.csv")

actual = df["OBS_RAINFALL"].values
nwp = df["TP_850"].values
meghova = df["MEGHOVA_PREDICTED_RAINFALL"].values


# ============================================================
# RMSE AND MAE
# ============================================================

def calculate_basic_metrics(actual, predicted):

    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mae = mean_absolute_error(actual, predicted)

    return rmse, mae


# ============================================================
# EVENT METRICS
# ============================================================

def calculate_event_metrics(actual, predicted, threshold):

    actual_event = actual >= threshold
    predicted_event = predicted >= threshold

    hits = np.sum(actual_event & predicted_event)
    misses = np.sum(actual_event & ~predicted_event)
    false_alarms = np.sum(~actual_event & predicted_event)
    correct_negatives = np.sum(~actual_event & ~predicted_event)

    # POD
    if hits + misses == 0:
        pod = np.nan
    else:
        pod = hits / (hits + misses)

    # FAR
    if hits + false_alarms == 0:
        far = np.nan
    else:
        far = false_alarms / (hits + false_alarms)

    # CSI
    if hits + misses + false_alarms == 0:
        csi = np.nan
    else:
        csi = hits / (hits + misses + false_alarms)

    # ETS
    total = hits + misses + false_alarms + correct_negatives

    random_hits = (
        (hits + misses) *
        (hits + false_alarms)
    ) / total

    denominator = hits + misses + false_alarms - random_hits

    if denominator == 0:
        ets = np.nan
    else:
        ets = (hits - random_hits) / denominator

    return pod, far, csi, ets, hits, misses, false_alarms


# ============================================================
# PRINT BASIC METRICS
# ============================================================

print("\n")
print("=" * 70)
print("2026 MEGHOVA COMPLETE EVALUATION")
print("=" * 70)

nwp_rmse, nwp_mae = calculate_basic_metrics(actual, nwp)
meghova_rmse, meghova_mae = calculate_basic_metrics(actual, meghova)

print("\nBASIC METRICS")
print("-" * 70)

print(f"{'Metric':<15}{'NWP':>15}{'MEGHOVA':>15}")

print(f"{'RMSE (mm)':<15}{nwp_rmse:>15.4f}{meghova_rmse:>15.4f}")
print(f"{'MAE (mm)':<15}{nwp_mae:>15.4f}{meghova_mae:>15.4f}")


# ============================================================
# EVENT METRICS
# ============================================================

thresholds = [1, 5, 10]

print("\n")
print("=" * 70)
print("EVENT-BASED METRICS")
print("=" * 70)

for threshold in thresholds:

    print(f"\nRainfall threshold: >= {threshold} mm")
    print("-" * 70)

    nwp_results = calculate_event_metrics(
        actual,
        nwp,
        threshold
    )

    meghova_results = calculate_event_metrics(
        actual,
        meghova,
        threshold
    )

    nwp_pod, nwp_far, nwp_csi, nwp_ets, nwp_hits, nwp_misses, nwp_fa = nwp_results

    m_pod, m_far, m_csi, m_ets, m_hits, m_misses, m_fa = meghova_results

    print(f"{'Metric':<15}{'NWP':>15}{'MEGHOVA':>15}")

    print(f"{'POD':<15}{nwp_pod:>15.4f}{m_pod:>15.4f}")
    print(f"{'FAR':<15}{nwp_far:>15.4f}{m_far:>15.4f}")
    print(f"{'CSI':<15}{nwp_csi:>15.4f}{m_csi:>15.4f}")
    print(f"{'ETS':<15}{nwp_ets:>15.4f}{m_ets:>15.4f}")

    print("\nContingency table counts:")

    print(
        f"NWP     → Hits: {nwp_hits}, "
        f"Misses: {nwp_misses}, "
        f"False Alarms: {nwp_fa}"
    )

    print(
        f"MEGHOVA → Hits: {m_hits}, "
        f"Misses: {m_misses}, "
        f"False Alarms: {m_fa}"
    )


# ============================================================
# SAVE RESULTS
# ============================================================

results = []

for threshold in thresholds:

    nwp_pod, nwp_far, nwp_csi, nwp_ets, _, _, _ = calculate_event_metrics(
        actual,
        nwp,
        threshold
    )

    m_pod, m_far, m_csi, m_ets, _, _, _ = calculate_event_metrics(
        actual,
        meghova,
        threshold
    )

    results.append({
        "THRESHOLD_MM": threshold,
        "NWP_RMSE": nwp_rmse,
        "MEGHOVA_RMSE": meghova_rmse,
        "NWP_MAE": nwp_mae,
        "MEGHOVA_MAE": meghova_mae,
        "NWP_POD": nwp_pod,
        "MEGHOVA_POD": m_pod,
        "NWP_FAR": nwp_far,
        "MEGHOVA_FAR": m_far,
        "NWP_CSI": nwp_csi,
        "MEGHOVA_CSI": m_csi,
        "NWP_ETS": nwp_ets,
        "MEGHOVA_ETS": m_ets
    })


results_df = pd.DataFrame(results)

results_df.to_csv(
    "meghova_2026_all_metrics.csv",
    index=False
)

print("\n")
print("=" * 70)
print("RESULTS SAVED")
print("=" * 70)

print("\nFile:")
print("meghova_2026_all_metrics.csv")