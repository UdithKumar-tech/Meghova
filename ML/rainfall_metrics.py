import pandas as pd
import numpy as np

# Load the untouched test results
df = pd.read_csv("meghova_proper_test_results.csv")

observed = df["OBS_RAINFALL"].astype(float)
raw_nwp = df["TP_850"].astype(float)
corrected = df["CORRECTED_RAINFALL"].astype(float)


def calculate_metrics(observed, predicted, threshold):

    obs_event = observed >= threshold
    pred_event = predicted >= threshold

    hits = ((obs_event) & (pred_event)).sum()
    misses = ((obs_event) & (~pred_event)).sum()
    false_alarms = ((~obs_event) & (pred_event)).sum()
    correct_negatives = ((~obs_event) & (~pred_event)).sum()

    total = len(observed)

    # Probability of Detection
    if hits + misses > 0:
        pod = hits / (hits + misses)
    else:
        pod = 0

    # False Alarm Ratio
    if hits + false_alarms > 0:
        far = false_alarms / (hits + false_alarms)
    else:
        far = 0

    # Critical Success Index
    if hits + misses + false_alarms > 0:
        csi = hits / (hits + misses + false_alarms)
    else:
        csi = 0

    # Equitable Threat Score
    random_hits = (
        (hits + misses) *
        (hits + false_alarms)
    ) / total

    if (
        hits + misses + false_alarms - random_hits
    ) > 0:
        ets = (
            hits - random_hits
        ) / (
            hits + misses + false_alarms - random_hits
        )
    else:
        ets = 0

    return {
        "Threshold": threshold,
        "Observed Events": int(obs_event.sum()),
        "Hits": int(hits),
        "Misses": int(misses),
        "False Alarms": int(false_alarms),
        "Correct Negatives": int(correct_negatives),
        "POD": pod,
        "FAR": far,
        "CSI": csi,
        "ETS": ets
    }


thresholds = [0.1, 1, 5, 10]

results = []

for threshold in thresholds:

    raw_metrics = calculate_metrics(
        observed,
        raw_nwp,
        threshold
    )

    corrected_metrics = calculate_metrics(
        observed,
        corrected,
        threshold
    )

    results.append({
        "Threshold": threshold,
        "Observed Events": raw_metrics["Observed Events"],

        "NWP_Hits": raw_metrics["Hits"],
        "NWP_Misses": raw_metrics["Misses"],
        "NWP_False_Alarms": raw_metrics["False Alarms"],
        "NWP_POD": raw_metrics["POD"],
        "NWP_FAR": raw_metrics["FAR"],
        "NWP_CSI": raw_metrics["CSI"],
        "NWP_ETS": raw_metrics["ETS"],

        "MEGHOVA_Hits": corrected_metrics["Hits"],
        "MEGHOVA_Misses": corrected_metrics["Misses"],
        "MEGHOVA_False_Alarms": corrected_metrics["False Alarms"],
        "MEGHOVA_POD": corrected_metrics["POD"],
        "MEGHOVA_FAR": corrected_metrics["FAR"],
        "MEGHOVA_CSI": corrected_metrics["CSI"],
        "MEGHOVA_ETS": corrected_metrics["ETS"]
    })


results_df = pd.DataFrame(results)


print("\n")
print("=" * 100)
print("MEGHOVA RAINFALL EVENT METRICS")
print("=" * 100)

for _, row in results_df.iterrows():

    print("\n" + "-" * 80)
    print(f"Threshold: {row['Threshold']} mm")
    print(f"Observed events: {row['Observed Events']}")

    print("\nRAW NWP")
    print("Hits:", row["NWP_Hits"])
    print("Misses:", row["NWP_Misses"])
    print("False Alarms:", row["NWP_False_Alarms"])
    print("POD:", round(row["NWP_POD"], 4))
    print("FAR:", round(row["NWP_FAR"], 4))
    print("CSI:", round(row["NWP_CSI"], 4))
    print("ETS:", round(row["NWP_ETS"], 4))

    print("\nMEGHOVA")
    print("Hits:", row["MEGHOVA_Hits"])
    print("Misses:", row["MEGHOVA_Misses"])
    print("False Alarms:", row["MEGHOVA_False_Alarms"])
    print("POD:", round(row["MEGHOVA_POD"], 4))
    print("FAR:", round(row["MEGHOVA_FAR"], 4))
    print("CSI:", round(row["MEGHOVA_CSI"], 4))
    print("ETS:", round(row["MEGHOVA_ETS"], 4))


print("\n")
print("=" * 100)
print("COMPACT RESULTS TABLE")
print("=" * 100)

display_columns = [
    "Threshold",
    "Observed Events",
    "NWP_POD",
    "MEGHOVA_POD",
    "NWP_FAR",
    "MEGHOVA_FAR",
    "NWP_CSI",
    "MEGHOVA_CSI",
    "NWP_ETS",
    "MEGHOVA_ETS"
]

print(
    results_df[display_columns]
    .round(4)
    .to_string(index=False)
)


results_df.to_csv(
    "meghova_rainfall_metrics.csv",
    index=False
)

print("\nSaved:")
print("meghova_rainfall_metrics.csv")