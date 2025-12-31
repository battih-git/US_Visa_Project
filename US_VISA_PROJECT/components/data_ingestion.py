import os, sys

import pandas as pd
from sklearn.model_selection import train_test_split

from US_VISA_PROJECT.entity.config_entity import DataIngestionConfig
from US_VISA_PROJECT.entity.artifact_entity import DataIngestionAritifact
from US_VISA_PROJECT.exception import USvisaException
from US_VISA_PROJECT.logger import logging
from US_VISA_PROJECT.data_access.usvisa_data import USvisaData

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        ''':param data ingestion config: configuration for data ingestion '''

        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise USvisaException(e,sys) from e
        
    def export_data_into_feature_store(self) -> pd.DataFrame:
        '''
        Method Name: export data into feature store
        Description: This method exports data from mongodb to csv

        Output: data is returned as artifact of data ingestion components
        On Failure: Write an exception log and then raise exception 
        '''

        try:
            logging.info(f'Exporting data from Mongodb')
            us_visa_data = USvisaData()
            data_frame = us_visa_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f'Shape of dataframe: {data_frame.shape}')
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f'Saving exported data into feature store file path: {feature_store_file_path}')
            data_frame.to_csv(feature_store_file_path,index=False, header=True)
            return data_frame
        except Exception as e:
            raise USvisaException(e,sys) from e
        
    def split_data_as_train_test(self, dataframe:pd.DataFrame) -> None:
        '''
        Method Name: split_data_as_train_test
        Description: This method splits the dataframe into train and test based on split ratio

        Output: Folder is created in S3 bucket
        On Failure: Write an exception log and then raise an exception
        '''
        try:
            train_test, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info('Performed train test split on the dataframe')
            logging.info(
                'Exited split_data_as_train_test method of DataIngestion Class'
            )
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f'Exporting train and test file path')
            train_test.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
        except Exception as e:
            raise USvisaException(e,sys) from e
        
    def initiate_data_ingestion(self) -> DataIngestionAritifact:
        '''
        Method Name: initiate_data_ingestion
        Description: This method initiates the data ingestion components of training pipeline

        Output: train set and test set are returned as the artifiacts of data ingestion components
        On Failure: Write an exception log and then raise an exception
        '''

        logging.info('Entered initiate_data_ingestion method of DataIngestion Class')
        try:
            dataframe = self.export_data_into_feature_store()
            logging.info('Got the data from MongoDB')
            self.split_data_as_train_test(dataframe=dataframe)
            logging.info('Performed train test split')
            logging.info('Exited initiate_data_ingestion method from DataIngestion Class')
            data_ingestion_artifact = DataIngestionAritifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
                )
            logging.info(f'Data ingestion artiface: {data_ingestion_artifact}')
            return data_ingestion_artifact
        
        except Exception as e:
            raise USvisaException(e,sys) from e
