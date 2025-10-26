import os
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature

logger = get_logger(__name__)


class ModelTraining:

    def __init__(self, train_path, test_path, model_config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_config_path = model_config_path

    def load_and_split_data(self):
        try:
            logger.info(f"Loading data from {self.train_path} and {self.test_path}")
            df_train = load_data(self.train_path)
            df_test = load_data(self.test_path)

            X_train = df_train.drop("exam_score", axis=1)
            y_train = df_train["exam_score"]

            X_test = df_test.drop("exam_score", axis=1)
            y_test = df_test["exam_score"]

            logger.info("Data loaded and split into features and target variable")

            return X_train, y_train, X_test, y_test
        except Exception as e:
            raise CustomException("Error in loading and splitting data", e)

    def train_linear_regression(self, X_train, y_train):
        try:
            model = LinearRegression()
            model.fit(X_train, y_train)
            return model
        except Exception as e:
            raise CustomException("Error in training Linear Regression model", e)

    def evaluate_model(self, model, X_test, y_test):
        try:
            predictions = model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)

            logger.info(f"Model Evaluation - MSE: {mse}, R2: {r2}")

            return mse, r2
        except Exception as e:
            raise CustomException("Error in evaluating model", e)

    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_config_path), exist_ok=True)

            logger.info(f"Saving model to {self.model_config_path}")
            joblib.dump(model, self.model_config_path)
            logger.info(f"Model saved at {self.model_config_path}")
        except Exception as e:
            raise CustomException("Error in saving model", e)

    def run(self):
        try:
            mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")
            mlflow.set_experiment("EduWell_Student_Performance_Prediction")

            with mlflow.start_run():
                logger.info("Starting model training process")

                logger.info("Starting our MLFlow experiment")

                logger.info("Loading the training and testing data to MLFlow")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                X_train, y_train, X_test, y_test = self.load_and_split_data()
                model = self.train_linear_regression(X_train, y_train)
                mse, r2 = self.evaluate_model(model, X_test, y_test)
                self.save_model(model)

                logger.info("Logging the model and metrics to MLFlow")
                mlflow.log_artifact(self.model_config_path)

                mlflow.log_metric("mse", mse)
                mlflow.log_metric("r2", r2)

                logger.info("Model training process completed successfully")
        except Exception as e:
            raise CustomException("Error in model training process", e)


if __name__ == "__main__":
    model_trainer = ModelTraining(
        PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH
    )
    model_trainer.run()
