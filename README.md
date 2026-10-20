# 🏡 Smart Home Energy AI

A machine learning web application that predicts household appliance energy consumption based on indoor conditions and outdoor weather readings.

## 📌 Project Overview

Smart Home Energy AI uses **Ridge Regression** to estimate appliance energy consumption in watt-hours (Wh). Users can enter a few environmental readings through an interactive Streamlit interface and receive an instant prediction.

## 🌐 Live Demo

Try the application here: [Smart Home Energy AI](https://home-energy-consumption.streamlit.app/)

## ✨ Features

- Predict household appliance energy consumption.
- Simple interface with only 8 user inputs.
- Dark mode and light mode.
- Interactive energy prediction gauge.
- Displays the prediction, typical dataset average, and model evaluation error.
- Responsive layout built with Streamlit.

## 📊 Dataset

- **Dataset:** Appliances Energy Prediction
- **Source:** UCI Machine Learning Repository
- **Records:** 19,735
- **Original columns:** 29
- **Target variable:** `Appliances` — household appliance energy consumption in Wh.

[Download the dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/00374/energydata_complete.csv)

## 🤖 Machine Learning

Five regression algorithms were evaluated using 10-fold cross-validation.

| Algorithm | Mean RMSE (Wh) |
|---|---:|
| Ridge Regression | 93.69 |
| Lasso Regression | 94.63 |
| Elastic Net | 97.24 |
| Support Vector Regression (SVR) | 100.88 |
| AdaBoost Regression | 189.75 |

**Selected model:** Ridge Regression, which achieved the lowest mean RMSE among the five tested algorithms.

## 🛠️ Technology Stack

- Python
- Pandas
- Scikit-learn
- Streamlit
- Pickle
- Google Colab

## 📁 Project Structure

```text
HomeEnergyConsumption/
├── app.py
├── energy_model.pkl
├── requirements.txt
└── README.md
```

## 🚀 Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/faiqaimtiaz207-ui/HomeEnergyConsumption.git
```

**2. Open the project folder**

```bash
cd HomeEnergyConsumption
```

**3. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**4. Start the application**

```bash
python -m streamlit run app.py
```

The application will open in your browser, usually at `http://localhost:8501`.

## ☁️ Deployment

This application can be deployed using [Streamlit Community Cloud](https://share.streamlit.io/).

1. Push `app.py`, `energy_model.pkl`, and `requirements.txt` to GitHub.
2. Sign in to Streamlit Community Cloud using GitHub.
3. Create a new app and select this repository.
4. Choose `app.py` as the main file.
5. Click **Deploy**.

## 📈 Evaluation

The models were compared using 10-fold cross-validation and Root Mean Squared Error (RMSE). Lower RMSE indicates better prediction performance on the evaluated data.

The selected Ridge Regression model achieved a mean RMSE of approximately **93.69 Wh**.

## ⚠️ Disclaimer

Predictions are estimates based on historical dataset patterns. They are not live electricity measurements, and actual household consumption may differ.

## 👩‍💻 Author

Developed as part of a Machine Learning assignment.
