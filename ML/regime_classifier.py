import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier


# 1. Load dataset
df = pd.read_csv("data/meghova_training_data.csv")

# Convert date
df["VT"] = pd.to_datetime(df["VT"])

# Extract month
df["MONTH"] = df["VT"].dt.month


# 2. Select features
features = [
    "LAT", "LON", "MONTH",

    "GH_850", "T_850", "RH_850",
    "U_850", "V_850", "TP_850", "CAPE_850",

    "GH_500", "T_500", "RH_500",
    "U_500", "V_500", "TP_500", "CAPE_500"
]

X = df[features]
y = df["WEATHER_REGIME"]


# 3. Encode regime names
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)


# 4. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)


# 5. XGBoost classifier
model = XGBClassifier(
    n_estimators=150,
    max_depth=3,
    learning_rate=0.05,
    objective="multi:softprob",
    num_class=5,
    eval_metric="mlogloss",
    random_state=42
)


# 6. Train
model.fit(X_train, y_train)


# 7. Evaluate
predictions = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        target_names=encoder.classes_,
        zero_division=0
    )
)


# 8. Save model
joblib.dump(model, "regime_classifier.pkl")
joblib.dump(encoder, "regime_label_encoder.pkl")

print("\nModel saved:")
print("regime_classifier.pkl")
print("regime_label_encoder.pkl")