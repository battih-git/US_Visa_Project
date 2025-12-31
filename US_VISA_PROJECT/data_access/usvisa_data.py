from US_VISA_PROJECT.configuration.mongo_db_connection import MongoDBClient
from US_VISA_PROJECT.constants import DATABASE_NAME, CONNECTION_URL
from US_VISA_PROJECT.exception import USvisaException
from US_VISA_PROJECT.logger import logging
import pandas as pd
import sys
from typing import Optional
import numpy as np

class USvisaData:
    """
    This class help to export entire mongo db record as pandas dataframe
    """

    def __init__(self):
        """
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise USvisaException(e,sys)
        

    def export_collection_as_dataframe(self,collection_name:str,database_name:Optional[str]=None)->pd.DataFrame:
        try:
            """
            export entire collectin as dataframe:
            return pd.DataFrame of collection
            """
            if database_name is None:
                collection = self.mongo_client.database[CONNECTION_URL]
            else:
                collection = self.mongo_client[database_name][CONNECTION_URL]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise USvisaException(e,sys)