import pandas as pd

# Load raw NWP data
df = pd.read_csv("data/karnataka_nwp_2026.csv")

# Convert forecast time
df["VT"] = pd.to_datetime(df["VT"])

rows = []

# Process every location + forecast date
for (lat, lon, vt), group in df.groupby(["LAT", "LON", "VT"]):

    row = {
        "LAT": lat,
        "LON": lon,
        "VT": vt.strftime("%Y-%m-%d")
    }

    # Get 850 hPa row
    r850 = group[group["PL"] == 850].iloc[0]

    # Get 500 hPa row
    r500 = group[group["PL"] == 500].iloc[0]

    # 850 hPa
    row["GH_850"] = r850["GH"]
    row["T_850"] = r850["T"] + 273.15
    row["RH_850"] = r850["RH"]
    row["U_850"] = r850["U"]
    row["V_850"] = r850["V"]
    row["TP_850"] = r850["TP"]
    row["CAPE_850"] = r850["CAPE"]

    # 500 hPa
    row["GH_500"] = r500["GH"]
    row["T_500"] = r500["T"] + 273.15
    row["RH_500"] = r500["RH"]
    row["U_500"] = r500["U"]
    row["V_500"] = r500["V"]
    row["TP_500"] = r500["TP"]
    row["CAPE_500"] = r500["CAPE"]

    rows.append(row)

# Create final MEGHOVA input
output = pd.DataFrame(rows)

output.to_csv(
    "data/future_nwp_input.csv",
    index=False
)

print("All MEGHOVA input rows created successfully!")
print("Total forecast cases:", len(output))
print(output.to_string(index=False))