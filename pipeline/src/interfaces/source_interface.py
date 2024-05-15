import os
from ..utils import query_reader
from ..constants import SCHEMA_FILE_PATH, STD_FILE_PATH, FINAL_FILE_PATH


class SourceInterface:
    def get_total_data_count(self, *args):
        """Extract total count of data present"""
        pass


    def get_data_from_response(self, *args):
        """Extract data from the response"""
        pass


    def create_tables(self, database = None):
        if not database:
            print("No Database Provided for Table creation !!!")
            return
        for file in os.listdir(SCHEMA_FILE_PATH):
            if file.endswith('.sql'):
                query = query_reader(f"{SCHEMA_FILE_PATH}{file}")
                database.execute_query(query)


    def extract_data(self, *args, **kwargs) -> None:
        """Extract data from the source"""
        pass


    def insert_into_raw_tables(self, *args, database = None) -> None:
        if not database:
            print("No Database Provided for data insertion in raw table !!!")
            return
        try:
            for file in os.listdir(SCHEMA_FILE_PATH):
                if file.endswith('.sql'):
                    query = query_reader(f"{SCHEMA_FILE_PATH}{file}")
                    database.batch_execute_queries(query, args)
        except Exception as error:
            print("Error while inserting into raw tables:", error)


    def insert_into_std_tables(self, database = None) -> None:
        if not database:
            print("No Database Provided for data insertion in standard table !!!")
            return
        try:
            for file in os.listdir(STD_FILE_PATH):
                if file.endswith('.sql'):
                    query = query_reader(f"{STD_FILE_PATH}{file}")
                    database.execute_query(query)
        except Exception as error:
            print("Error while inserting into std tables:", error)


    def insert_into_final_tables(self, database = None) -> None:
        if not database:
            print("No Database Provided for data insertion in final table !!!")
            return
        try:
            for file in os.listdir(FINAL_FILE_PATH):
                if file.endswith('.sql'):
                    print(f"Inserting data into {' '.join(file.replace(".sql", '').split('_')[1:])}")
                    query = query_reader(f"{FINAL_FILE_PATH}{file}")
                    database.execute_query(query)
        except Exception as error:
            print("Error while inserting into std tables:", error)
