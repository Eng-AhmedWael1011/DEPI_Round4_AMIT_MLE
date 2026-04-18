# FindDonorsAI — Census Income Prediction System

A production-ready full-stack ML web application that predicts whether a person's income exceeds $50K using the Census "Finding Donors" dataset.

## 🧠 Features

- **CatBoost ML Model** — Trained with GridSearchCV hyperparameter tuning and SMOTE for class imbalance
- **Flask REST API** — Modular backend with prediction, metrics, data summary, and feature importance endpoints
- **React + D3.js Frontend** — Interactive dashboards with animated visualizations
- **SHAP Explainability** — Feature importance analysis using SHAP TreeExplainer
- **Premium Dark UI** — Glassmorphism design with smooth animations

## 📊 Model Performance

| Metric    | Score  |
|-----------|--------|
| Accuracy  | 85.4%  |
| Precision | 71.0%  |
| Recall    | 72.0%  |
| F1 Score  | 71.5%  |
| F-beta    | 71.2%  |

## 🏗️ Project Structure

```
P2/
├── backend/
│   ├── app.py              # Flask entry point
│   ├── config.py            # Configuration
│   ├── Procfile             # Render deployment
│   ├── requirements.txt     # Python dependencies
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   ├── pipeline/            # ML pipeline modules
│   ├── models/              # Saved model artifacts
│   └── utils/               # Helper functions
├── frontend/
│   ├── src/
│   │   ├── components/      # React UI components
│   │   ├── pages/           # Dashboard & Prediction pages
│   │   ├── services/        # API client
│   │   ├── App.jsx          # Root component
│   │   └── App.css          # Design system
│   └── package.json
├── data/
│   └── census.csv           # Dataset
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Train the model (first time only)
python pipeline/pipeline.py

# Start the API server
python app.py
```

The API will be available at `http://localhost:5000`.

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## 📡 API Endpoints

| Method | Endpoint            | Description                          |
|--------|---------------------|--------------------------------------|
| GET    | `/`                 | Health check                         |
| POST   | `/predict`          | Predict income from user features    |
| GET    | `/metrics`          | Get model evaluation metrics         |
| GET    | `/data-summary`     | Get dataset summary statistics       |
| GET    | `/feature-importance` | Get SHAP feature importance values |

### POST /predict — Example

```json
// Request
{
  "age": 39,
  "workclass": "State-gov",
  "education_level": "Bachelors",
  "education-num": 13,
  "marital-status": "Never-married",
  "occupation": "Adm-clerical",
  "relationship": "Not-in-family",
  "race": "White",
  "sex": "Male",
  "capital-gain": 2174,
  "capital-loss": 0,
  "hours-per-week": 40,
  "native-country": "United-States"
}

// Response
{
  "prediction": "<=50K",
  "probability": 0.2341
}
```

## ☁️ Deploying on Render

### Backend Deployment

1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Root Directory**: `backend/`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3
4. Add environment variables:
   - `FLASK_ENV=production`
   - `FLASK_DEBUG=0`
   - `MODEL_PATH=models`
   - `DATA_PATH=../data`
   - `CORS_ORIGINS=https://your-frontend-url.onrender.com`
5. Deploy!

> **Note**: Make sure the `models/` directory with trained artifacts and `data/census.csv` are committed to the repository, or train the model as part of the build step.

### Frontend Deployment

1. Create a new **Static Site** on Render
2. Connect the same repository
3. Configure:
   - **Root Directory**: `frontend/`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
4. Add environment variable:
   - `VITE_API_URL=https://your-backend-url.onrender.com`
5. Deploy!

## 🛠️ Tech Stack

**Backend**: Python, Flask, CatBoost, scikit-learn, SMOTE (imbalanced-learn), SHAP, joblib  
**Frontend**: React, Bootstrap 5, D3.js, Axios, React Router  
**Deployment**: Gunicorn, Render

## 📝 License

This project is part of the DEPI Machine Learning Engineer program.
