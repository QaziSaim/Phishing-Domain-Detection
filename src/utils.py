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
def evaluate_model(model, x_train, x_test, y_train, y_test):
    '''The function will take model, x train, x test, y train, y test
    and then it will fit the model, then make predictions on the trained model,
    it will then print roc-auc score of train and test, then plot the roc, auc curve,
    print confusion matrix for train and test, then print classification report for train and test,
    then plot the feature importances if the model has feature importances,
    and finally it will return the following scores as a list:
    recall_train, recall_test, acc_train, acc_test, F1_train, F1_test
    '''
    try:
        # Fit the model to the training data.
        model.fit(x_train, y_train)

        # make predictions on the test data
        y_pred_train = model.predict(x_train)
        y_pred_test = model.predict(x_test)

        # calculate confusion matrix
        cm_train = confusion_matrix(y_train, y_pred_train)
        cm_test = confusion_matrix(y_test, y_pred_test)

        fig, ax = plt.subplots(1, 2, figsize=(11,4))

        print("\nConfusion Matrix:")
        sns.heatmap(cm_train, annot=True, xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'], cmap="Oranges", fmt='.4g', ax=ax[0])
        ax[0].set_xlabel("Predicted Label")
        ax[0].set_ylabel("True Label")
        ax[0].set_title("Train Confusion Matrix")

        sns.heatmap(cm_test, annot=True, xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'], cmap="Oranges", fmt='.4g', ax=ax[1])
        ax[1].set_xlabel("Predicted Label")
        ax[1].set_ylabel("True Label")
        ax[1].set_title("Test Confusion Matrix")

        plt.tight_layout()
        plt.show()


        # calculate classification report
        cr_train = classification_report(y_train, y_pred_train, output_dict=True)
        cr_test = classification_report(y_test, y_pred_test, output_dict=True)
        print("\nTrain Classification Report:")
        crt = pd.DataFrame(cr_train).T
        print(crt.to_markdown())
        # sns.heatmap(pd.DataFrame(cr_train).T.iloc[:, :-1], annot=True, cmap="Blues")
        print("\nTest Classification Report:")
        crt2 = pd.DataFrame(cr_test).T
        print(crt2.to_markdown())
        # sns.heatmap(pd.DataFrame(cr_test).T.iloc[:, :-1], annot=True, cmap="Blues")

        precision_train = cr_train['weighted avg']['precision']
        precision_test = cr_test['weighted avg']['precision']

        recall_train = cr_train['weighted avg']['recall']
        recall_test = cr_test['weighted avg']['recall']

        acc_train = accuracy_score(y_true = y_train, y_pred = y_pred_train)
        acc_test = accuracy_score(y_true = y_test, y_pred = y_pred_test)

        F1_train = cr_train['weighted avg']['f1-score']
        F1_test = cr_test['weighted avg']['f1-score']

        model_score = [precision_train, precision_test, recall_train, recall_test, acc_train, acc_test, F1_train, F1_test ]
        return model_score
    except Exception as e:
        logging.info("Exception occured during model training")
        raise CustomException(e,sys)