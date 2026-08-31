# KrishiSakhi — AI-Powered Price Prediction for Agriculture Products

A ready-to-run Flask + LSTM project implementing the 8 core algorithms of the
price prediction pipeline.

## Project Structure & Algorithm Map

| File | Algorithm |
|---|---|
| `utils/preprocessing.py` | **Algorithm 1** — Data Preprocessing & Cleaning |
| `utils/model_loader.py` | **Algorithm 2** — Model & Scaler Loading |
| `utils/sequence_prep.py` | **Algorithm 3** — Feature Extraction & Sequence Preparation |
| `train_model.py` | **Algorithm 4** — LSTM Model Training |
| `utils/predictor.py` | **Algorithm 5** — Rolling-Window Multi-Month Prediction (main logic) |
| `app.py` | **Algorithm 6** — Backend Prediction API (Flask) |
| `static/script.js` (renderTable) | **Algorithm 7** — Frontend Table Rendering |
| `static/script.js` (renderChart) | **Algorithm 8** — Graph/Chart Visualization |

## Included Sample Data
Synthetic 7.5-year monthly datasets (month, year, rainfall, price) are provided
for three crops so the project runs out of the box:
- `data/rice.csv`
- `data/wheat.csv`
- `data/onion.csv`

Replace these with real Agmarknet/market data any time — same column format
(`month, year, rainfall, price`) is all that's required.

## Setup

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the LSTM model for each crop (Algorithm 4)
python train_model.py all
# or individually:
python train_model.py rice
python train_model.py wheat
python train_model.py onion

# 4. Run the web app
python app.py
```

Then open **http://localhost:5000** in your browser, pick a crop, enter
months-ahead, and click **Predict Price** to see the table (Algorithm 7) and
line chart (Algorithm 8) update.

## Notes
- Trained models are saved under `models/` as `<crop>_lstm.keras` plus
  `<crop>_x_scaler.pkl` / `<crop>_y_scaler.pkl` (Algorithm 2 loads these).
- To add a new crop, drop a CSV with the same 4 columns into `data/`, then run
  `python train_model.py <cropname>`.
- `months_ahead` is capped at 24 in `predictor.py` — adjust `predict_future_prices`
  if you need longer-range forecasts.
