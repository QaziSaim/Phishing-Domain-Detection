
import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException  

from sklearn.impute import SimpleImputer # handling missing value
from sklearn.preprocessing import StandardScaler # handling feature scaling
# Whenever our categorical feature have rank we use ordinal encoding
from sklearn.preprocessing import OrdinalEncoder # Feature Engineering audinal encoding
## Pipelines :-> is for combining multiple steps
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer # Grouping the thing
# from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')
    # pickle file : model which we create to save it in hard drive -- serailized file
