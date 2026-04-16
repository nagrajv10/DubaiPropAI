# 🇦🇪 DubaiPropAI

**DubaiPropAI** is an end-to-end, production-grade Artificial Intelligence application for predicting real estate investment metrics specifically designed for the Dubai property market.

It simulates a full-stack prop-tech architecture utilizing an **XGBoost Machine Learning Pipeline**, a **FastAPI** backend, and a dynamic **React + TailwindCSS** dashboard, completely orchestrated via Docker.

---

## 🏗️ Architecture Stack

This repository is structured as a monorepo containing multiple decoupled layers:

*   **Frontend (`/fe`)**: React.js, Vite, TypeScript, and TailwindCSS 3. Builds a glassmorphism-styled dashboard serving dynamic metric cards.
*   **Backend (`/be`)**: Python, FastAPI, SQLAlchemy, and Pydantic. Securely exposes REST endpoints for predictions and database mutations.
*   **Machine Learning (`/ml`)**: Python, Pandas, Scikit-learn, XGBoost. Sandbox for generating simulated market data, training prediction models, and generating `joblib` artifacts.
*   **Database**: PostgreSQL integrated with Alembic for clean structural migrations.
*   **Containerization**: Unified with `docker-compose` to manage the bridge network linking the React web server, FastAPI inference server, and PostgreSQL database.

---

## 🚀 Getting Started

The easiest way to bootstrap the entire environment locally is via Docker.

### Prerequisites

*   [Docker Desktop](https://www.docker.com/products/docker-desktop) (Running)
*   Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/DubaiPropAI.git
   cd DubaiPropAI
   ```

2. **Build and spin up the Docker Cluster:**
   ```bash
   docker-compose up --build -d
   ```
   > This command spins up a Postgres Database (`db`), builds the FastAPI backend (`backend`), and launches the NGINX-served React frontend (`frontend`).

3. **Monitor the logs (Optional):**
   ```bash
   docker-compose logs -f
   ```

---

## 🌐 Accessing the Application

Once your Docker containers are actively running, you can interact with the various endpoints natively through your web browser.

#### 1. The Interactive Dashboard
*   **URL**: [http://localhost](http://localhost)
*   **Description**: Play around with the React frontend! Alter the square footage, bedrooms, or Dubai sub-areas like *Marina* or *JVC* and get immediate AI-based predictions.

#### 2. The API Root
*   **URL**: [http://localhost:8000/health](http://localhost:8000/health)
*   **Description**: Quick health check ensuring the backend handles requests and the model is loaded.

#### 3. Automatic Swagger UI
*   **URL**: [http://localhost:8000/docs](http://localhost:8000/docs)
*   **Description**: Test out backend API endpoints (`POST /predict`, `GET /properties`) safely without opening the frontend. Provided natively by FastAPI.

---

## 🤖 ML Pipeline Details

The models predict three core investment variables based on inputs (`area`, `property_type`, `size_sqft`, `bedrooms`):
1. **Estimated Price (AED)**
2. **Current Rental Yield (%)**
3. **5-Year ROI (%)**

The training pipeline requires a CSV. Out of the box, we use a simulation script to seed robust fake transaction data across the city.
*   `ml/generate_data.py`: Mocks 2,000 realistic listings and exports to `ml/data/dubai_properties.csv`.
*   `ml/train_model.py`: Ingests the CSV, trains the pipelines, scores the mean absolute errors (MAE), and securely saves to `ml/models/models.joblib`. 

*(Both run cleanly out of box, but can be altered whenever you collect scraped real property data!)*
