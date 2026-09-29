Markdown

# MEGHOVA — Machine Learning Contribution

This folder contains my Machine Learning contribution to the MEGHOVA project.

## Machine Learning Overview

The ML component of MEGHOVA improves existing Numerical Weather Prediction (NWP) rainfall forecasts using rainfall regime classification and regime-specific bias correction.

The overall ML pipeline is:

```text
NWP Atmospheric Data
        ↓
Feature Preparation
        ↓
Rainfall Regime Classification
        ↓
Predicted Rainfall Regime
        ↓
Regime-Specific Expert Model
        ↓
Predicted Rainfall Correction
        ↓
NWP Rainfall + Correction
        ↓
MEGHOVA Rainfall Forecast
Rainfall Regime Classification
An XGBoost multi-class classifier is used to identify the current rainfall regime from NWP and atmospheric features.

Input Features
Latitude

Longitude

Month

850 hPa geopotential height

850 hPa temperature

850 hPa relative humidity

850 hPa U and V wind components

850 hPa NWP rainfall

850 hPa CAPE

500 hPa geopotential height

500 hPa temperature

500 hPa relative humidity

500 hPa U and V wind components

500 hPa NWP rainfall

500 hPa CAPE

Rainfall Regimes
The classifier predicts five regimes:

ACTIVE

BREAK

NORMAL

DEPRESSION

COASTAL_OROGRAPHIC

Model
XGBoost Multi-Class Classifier

The trained classifier and label encoder are stored as:


regime_classifier.pkl
regime_label_encoder.pkl
Regime-Specific Rainfall Bias Correction
After identifying the rainfall regime, the corresponding expert model is selected to estimate the correction required for the original NWP rainfall forecast.

The correction target is:


Correction = Observed Rainfall − NWP Rainfall
Five XGBoost regression expert models were developed for the different rainfall regimes.

The predicted correction is added to the original NWP rainfall:


MEGHOVA Rainfall
=
NWP Rainfall + Predicted Correction
Negative corrected rainfall values are clipped to zero.

Expert Models

experts/
├── active_expert.pkl
├── break_expert.pkl
├── normal_expert.pkl
├── depression_expert.pkl
└── coastal_orographic_expert.pkl
Integrated Prediction Pipeline

             NWP Forecast
                   ↓
          Atmospheric Features
                   ↓
       XGBoost Regime Classifier
                   ↓
           Predicted Regime
                   ↓
        Select Expert Model
                   ↓
       Predict Rainfall Correction
                   ↓
       Add Correction to NWP
                   ↓
         MEGHOVA Forecast
The important point is that MEGHOVA post-processes the existing NWP forecast rather than replacing the NWP model.

Time-Based Evaluation
To evaluate the model on unseen future data, the dataset was divided chronologically:

Training period: 2021–2024

Unseen test period: 2025

Regime Classification Results
Metric	Result
Accuracy	90.83%
Macro F1	0.74
Weighted F1	0.90

Rainfall Forecast Results
Model	RMSE
Original NWP	0.3726 mm
MEGHOVA	0.0957 mm

RMSE reduction: 74.31%

Event Verification
Threshold	Model	POD	FAR	CSI	ETS
≥1 mm	NWP	0.9474	0	0.9474	0.9381
≥1 mm	MEGHOVA	1.0000	0	1.0000	1.0000
≥5 mm	NWP	0.8182	0	0.8182	0.8034
≥5 mm	MEGHOVA	0.9091	0	0.9091	0.9008
≥10 mm	NWP	0.8000	0	0.8000	0.7931
≥10 mm	MEGHOVA	1.0000	0	1.0000	1.0000

The ≥10 mm results are based on only five observed events and therefore have limited statistical strength.

2026 Verification
The ML pipeline was additionally tested on a 2026 verification dataset containing 10 forecast cases.

Metric	NWP	MEGHOVA
RMSE	2.7977 mm	3.0704 mm
MAE	2.3500 mm	2.6968 mm

For this small 2026 sample, the original NWP forecast had lower RMSE and MAE. This result is included for transparent evaluation of the current model.

ML Files
Core ML

regime_classifier.py
train_experts.py
predict_meghova.py
future_prediction.py
prepare_2026_input.py
Evaluation

time_based_evaluation.py
rainfall_metrics.py
time_based_rainfall_metrics.py
evaluate_2026.py
evaluate_2026_all_metrics.py
evaluate_meghova.py
proper_evaluation.py
final_evaluation.py
Trained Models

regime_classifier.pkl
regime_label_encoder.pkl

experts/
├── active_expert.pkl
├── break_expert.pkl
├── normal_expert.pkl
├── depression_expert.pkl
└── coastal_orographic_expert.pkl
Current Limitations
The model requires NWP atmospheric inputs to make a rainfall prediction.

Latitude, longitude and date alone are not sufficient.

The current model has mainly been validated for 1-day-ahead forecasts.

The BREAK regime has limited training examples.

The 2026 verification dataset contains only 10 cases.

More spatial and temporal data is required for stronger validation.

The current 2026 verification is a small-sample evaluation and should not be treated as a definitive performance estimate.

Summary
My ML contribution to MEGHOVA covers the complete post-processing pipeline:

NWP data → rainfall regime classification → regime-specific bias correction → corrected rainfall forecast → model evaluation and verification.




