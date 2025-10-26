import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.preprocessing import StandardScaler

logger = get_logger(__name__)


class DataProcessor:

    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir, exist_ok=True)

    def preprocess_data(self, df):
        try:
            logger.info("Starting the preprocessing of data")

            logger.info("Fill out missing values")
            df["parental_education_level"] = df["parental_education_level"].fillna(
                df["parental_education_level"].mode()[0]
            )

            logger.info("Dropping the columns")
            df.drop(columns=["student_id"], inplace=True)
            df.drop_duplicates(inplace=True)

            cat_col = self.config["data_processing"]["categoraical_features"]
            num_col = self.config["data_processing"]["numerical_features"]

            logger.info(
                f"Apply label and one hot encoding to categorical columns: {cat_col}"
            )

            diet_quality = {"Poor": 0, "Fair": 1, "Good": 2}
            parental_education_level = {"High School": 0, "Bachelor": 1, "Master": 2}
            internet_quality = {"Poor": 0, "Average": 1, "Good": 2}

            df["dq_e"] = df["diet_quality"].map(diet_quality)
            df["pel_e"] = df["parental_education_level"].map(parental_education_level)
            df["iq_e"] = df["internet_quality"].map(internet_quality)

            dummies = pd.get_dummies(
                df[["gender", "part_time_job", "extracurricular_participation"]],
                drop_first=True,
            )

            df = pd.concat([df, dummies], axis=1)

            return df

        except Exception as e:
            logger.error(f"Error during preprocessing: {e}")
            raise CustomException("Error during preprocessing", e)

    def feature_selection(self, df):
        try:
            logger.info("Starting feature selection")

            df = df.drop(
                [
                    "gender",
                    "part_time_job",
                    "diet_quality",
                    "parental_education_level",
                    "internet_quality",
                    "extracurricular_participation",
                ],
                axis=1,
            )

            logger.info("Feature selection completed")
            return df

        except Exception as e:
            logger.error(f"Error during feature selection: {e}")
            raise CustomException("Error during feature selection", e)

    def save_data(self, df, file_path):
        try:
            logger.info(f"Saving processed data to {file_path}")
            df.to_csv(file_path, index=False)
            logger.info("Data saved successfully")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise CustomException("Error saving data", e)

    def process(self):
        try:
            logger.info("Loading data from RAW directory")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.feature_selection(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)
            logger.info("Data processing completed successfully")

        except Exception as e:
            logger.error(f"Error in data processing: {e}")
            raise CustomException("Error in data processing", e)


if __name__ == "__main__":
    processor = DataProcessor(
        TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH
    )
    processor.process()
