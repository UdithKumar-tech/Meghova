import pandas as pd
import numpy as np


# ============================================================
# LOAD 2025 TIME-BASED TEST RESULTS
# ============================================================

df = pd.read_csv("meghova_time_based_test_results.csv")

observed = df["OBS_RAINFALL"].astype(float)
nwp = df["TP_850"].astype(float)
meghova = df["CORRECTED_RAINFALL"].astype(float)


# ============================================================
# METRIC FUNCTION
# ============================================================

def calculate_metrics(observed, predicted, threshold):

    actual_event = observed >= threshold
    predicted_event = predicted >= threshold

    hits = np.sum(actual_event & predicted_event)
    misses = np.sum(actual_event & ~predicted_event)
    false_alarms = np.sum(~actual_event & predicted_event)
    correct_negatives = np.sum(~actual_event & ~predicted_event)

    pod = (
        hits / (hits + misses)
        if (hits + misses) > 0
        else 0
    )

    far = (
        false_alarms / (hits + false_alarms)
        if (hits + false_alarms) > 0
        else 0
    )

    csi = (
        hits / (hits + misses + false_alarms)
        if (hits + misses + false_alarms) > 0
        else 0
    )

    total = hits + misses + false_alarms + correct_negatives

    random_hits = (
        ((hits + misses) * (hits + false_alarms)) / total
        if total > 0
        else 0
    )

    ets_denominator = (
        hits + misses + false_alarms - random_hits
    )

    ets = (
        (hits - random_hits) / ets_denominator
        if ets_denominator > 0
        else 0
    )

    return {
        "Hits": hits,
        "Misses": misses,
        "False Alarms": false_alarms,
        "POD": pod,
        "FAR": far,
        "CSI": csi,
        "ETS": ets
    }


# ============================================================
# CALCULATE METRICS
# ============================================================

thresholds = [1, 5, 10]

results = []

print("\n")
print("=" * 75)
print("TIME-BASED RAINFALL EVENT EVALUATION — 2025")
print("=" * 75)

for threshold in thresholds:

    nwp_metrics = calculate_metrics(
        observed,
        nwp,
        threshold
    )

    meghova_metrics = calculate_metrics(
        observed,
        meghova,
        threshold
    )

    print("\n")
    print("-" * 75)
    print(f"RAINFALL THRESHOLD: {threshold} mm")
    print("-" * 75)

    print("\nNWP:")
    print(
        f"Hits: {nwp_metrics['Hits']} | "
        f"Misses: {nwp_metrics['Misses']} | "
        f"False Alarms: {nwp_metrics['False Alarms']}"
    )

    print(
        f"POD: {nwp_metrics['POD']:.4f}"
    )

    print(
        f"FAR: {nwp_metrics['FAR']:.4f}"
    )

    print(
        f"CSI: {nwp_metrics['CSI']:.4f}"
    )

    print(
        f"ETS: {nwp_metrics['ETS']:.4f}"
    )

    print("\nMEGHOVA:")

    print(
        f"Hits: {meghova_metrics['Hits']} | "
        f"Misses: {meghova_metrics['Misses']} | "
        f"False Alarms: {meghova_metrics['False Alarms']}"
    )

    print(
        f"POD: {meghova_metrics['POD']:.4f}"
    )

    print(
        f"FAR: {meghova_metrics['FAR']:.4f}"
    )

    print(
        f"CSI: {meghova_metrics['CSI']:.4f}"
    )

    print(
        f"ETS: {meghova_metrics['ETS']:.4f}"
    )

    results.append({
        "Threshold_mm": threshold,

        "NWP_POD": nwp_metrics["POD"],
        "NWP_FAR": nwp_metrics["FAR"],
        "NWP_CSI": nwp_metrics["CSI"],
        "NWP_ETS": nwp_metrics["ETS"],

        "MEGHOVA_POD": meghova_metrics["POD"],
        "MEGHOVA_FAR": meghova_metrics["FAR"],
        "MEGHOVA_CSI": meghova_metrics["CSI"],
        "MEGHOVA_ETS": meghova_metrics["ETS"]
    })


# ============================================================
# SAVE RESULTS
# ============================================================

results_df = pd.DataFrame(results)

results_df.to_csv(
    "meghova_time_based_rainfall_metrics.csv",
    index=False
)

print("\n")
print("=" * 75)
print("FINAL METRICS TABLE")
print("=" * 75)

print(
    results_df.to_string(index=False)
)

print("\nSaved:")
print("meghova_time_based_rainfall_metrics.csv")