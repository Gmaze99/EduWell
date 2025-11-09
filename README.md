# EduWell

EduWell is a small end-to-end ML project demonstrating data ingestion, processing, model training, and a simple Flask web app to serve predictions.

## Highlights
- Data ingestion from GCS: [`src.data_ingestion.DataIngestion`](src/data_ingestion.py)
- Data preprocessing & feature engineering: [`src.data_processing.DataProcessor`](src/data_processing.py)
- Model training and MLflow logging: [`src.model_training.ModelTraining`](src/model_training.py)
- Flask app for predictions: [application.py](application.py)
- Centralized paths config: [config/paths_config.py](config/paths_config.py)
- Utilities: [utils/common_functions.py](utils/common_functions.py)
- Custom error handling: [`src.custom_exception.CustomException`](src/custom_exception.py)
- Pipeline orchestration entry: [pipeline/training_pipeline.py](pipeline/training_pipeline.py)

## Repository structure (selected)
- [application.py](application.py) - Flask app that loads the trained model and exposes a prediction form.
- [pipeline/training_pipeline.py](pipeline/training_pipeline.py) - Runs ingestion → processing → training.
- [src/data_ingestion.py](src/data_ingestion.py) - Data download/split logic (class: [`src.data_ingestion.DataIngestion`](src/data_ingestion.py)).
- [src/data_processing.py](src/data_processing.py) - Preprocessing and feature selection (class: [`src.data_processing.DataProcessor`](src/data_processing.py)).
- [src/model_training.py](src/model_training.py) - Model training, evaluation, saving (class: [`src.model_training.ModelTraining`](src/model_training.py)).
- [config/paths_config.py](config/paths_config.py) - Path constants used across the repo.
- [utils/common_functions.py](utils/common_functions.py) - YAML reader and CSV loader utilities.
- [static/style.css](static/style.css), [templates/index.html](templates/index.html) - Frontend for the Flask app.
- [Dockerfile](Dockerfile) - Container image build.
- [Jenkinsfile](Jenkinsfile) - CI/CD pipeline to build, push, and deploy to GKE.
- [requirements.txt](requirements.txt), [setup.py](setup.py)

## Quickstart (local)

1. Create virtual env and install
```bash
python -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

2. Run the end-to-end pipeline (ingest → process → train)
```bash
python pipeline/training_pipeline.py
```
This uses:
- [`src.data_ingestion.DataIngestion`](src/data_ingestion.py) to download and split raw data,
- [`src.data_processing.DataProcessor`](src/data_processing.py) to preprocess and save processed CSVs,
- [`src.model_training.ModelTraining`](src/model_training.py) to train and persist the model to the path in [config/paths_config.py](config/paths_config.py).

3. Start the Flask app
```bash
python application.py
```
Open http://localhost:8080 and use the form (UI in [templates/index.html](templates/index.html)).

## Docker
Build and run the image that serves the Flask app:
```bash
docker build -t eduwell:latest .
docker run -p 8080:8080 eduwell:latest
```
The [Dockerfile](Dockerfile) exposes port 8080 and installs the package in editable mode.

## MLflow & Model Logging
Training code logs artifacts and metrics via MLflow inside [`src.model_training.ModelTraining`](src/model_training.py). Adjust MLflow server/URI as needed in that module before running.

## CI/CD
The [Jenkinsfile](Jenkinsfile) demonstrates:
- building a venv,
- packaging the app,
- building & pushing Docker image to GCR,
- deploying to GKE (requires GCP credentials stored in Jenkins).

## Notes & troubleshooting
- Paths and filenames are centralized in [config/paths_config.py](config/paths_config.py).
- YAML config is read via [utils/common_functions.py](utils/common_functions.py). Missing config files will raise [`src.custom_exception.CustomException`](src/custom_exception.py).
- Logs are written to the `logs/` directory using the logger in `src/logger.py`.

## Contributing
- Follow the existing structure: ingestion → processing → training → serving.
- Add unit tests and use logging + `CustomException` for consistent error handling.
