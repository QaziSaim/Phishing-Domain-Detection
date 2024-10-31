import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
# import xgboost as xgb
from src.exception import CustomException
from src.logger import logging
from src.utils import evaluate_model
from src.utils import save_object
from dataclasses import dataclass
import sys
import os
# Step 6

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    def inititate_model_training(self,train_array,test_array):
        try:
            logging.info("Splitting Dependent and independent features from train and test")
            X_train,X_test,y_train,y_test = (
                train_array[:,:-1],
                test_array[:,:-1],
                train_array[:,-1],
                test_array[:,-1],
            )
            models={
                'LogisticRegression': LogisticRegression(),
                'DecisionTreeClassifier':DecisionTreeClassifier(),
                'GaussianNB':GaussianNB(),
                'SVC':SVC(),
                'RandomForestClassifier':RandomForestClassifier(),
                'MLPClassifier':MLPClassifier()
                }
            
        except Exception as e:
            logging.info("Some exception occured while training model")
            raise CustomException(e,sys)