# any common functionality are put in this
import sys
import os
import pickle # create pickle file from model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score,confusion_matrix,recall_score,classification_report

from src.exception import CustomException
from src.logger import logging



# step 5
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)
# Step 7
def evaluate_model(models,X_train,X_test,y_train,y_test):
    try:
        report = {}

        for i in range(len(models)):
            model = list(models.values())[i]

            # Train model
            model.fit(X_train,y_train)

            # predict training data
            # y_train_pred = model.predict(X_train)

            #predict Testing data
            y_pred = model.predict(X_test)

            # Get R2 scores for train and test data

            # train_model_score=r2_score(y_train,y_train_pred)
            test_model_score=recall_score(y_test,y_pred)

            report[list(models.keys())[i]] = test_model_score
        return report
    except Exception as e:
        logging.info("Exception occured during model training")
        raise CustomException(e,sys)

# Step 10.1
def load_objects(file_path):
    try:
        with open(file_path, 'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        logging.info("Exception occured during in load_objects function utils ")
        raise CustomException(e,sys)