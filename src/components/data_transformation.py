
import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException  
from sklearn.feature_selection import mutual_info_classif,SelectKBest
from sklearn.impute import SimpleImputer # handling missing value
from sklearn.preprocessing import StandardScaler # handling feature scaling
# Whenever our categorical feature have rank we use ordinal encoding
from sklearn.preprocessing import OrdinalEncoder # Feature Engineering audinal encoding
## Pipelines :-> is for combining multiple steps
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer # Grouping the thing
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')
    # pickle file : model which we create to save it in hard drive -- serailized file
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    def get_transformation_object(self):    
        try:
            logging.info("Data Transformation initiated")


            df = pd.read_csv(os.path.join('artifacts','train.csv'))
            numeric_features = df.columns.difference(['id', 'CLASS_LABEL'])
            #  # Step 1: Feature Selection (requires target variable)
            # selector = SelectKBest(mutual_info_classif, k=25)
            # X=numeric_features[:]
            
            # # y=df.iloc[::-1]
            # X_selected = selector.fit_transform(X)
            # selected_features = selector.get_support(indices=True) 


            numeric_pipeline=Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='mean')),
                    ('scalar',StandardScaler()),]
            )
            preprocessor = ColumnTransformer([
                ('pipeline',numeric_pipeline,numeric_features),
            ])
            logging.info("Pipeline Completed")
            return preprocessor
        
        except Exception as e:
            logging.error("Error in Data Transformation")
            raise CustomException(e,sys)
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read train and test data completed')
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head : \n{test_df.head().to_string()}')
            
            logging.info('Obtaining preprocessing object')
            preprocessing_obj = self.get_transformation_object()

            target_column_name = 'CLASS_LABEL'
            drop_columns= [target_column_name ,'id']

            input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df = test_df[target_column_name]

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr  = preprocessing_obj.transform(input_feature_test_df)
            logging.info('Applying preprocessing object on training and testing datasets.')
            # To read this quickly we need to store it in arrays format
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            logging.info('Preprocessor pickle file save')
            
            return(
                train_arr, test_arr,self.data_transformation_config.preprocessor_obj_file_path
            )

            
        except Exception as E:
            logging.info("Exception occured in the initiate data transformation")

            raise CustomException(E,sys)