import os
from ..utils import query_reader
from ..constants import SCHEMA_FILE_PATH, RAW_FILE_PATH, STD_FILE_PATH, FINAL_FILE_PATH


class SourceInterface:
    def create_tables(self, database):
        try:
            for file in os.listdir(SCHEMA_FILE_PATH):
                if file.endswith('.sql'):
                    query = query_reader(os.path.join(SCHEMA_FILE_PATH, file))
                    database.execute_query(query)
        except Exception as error:
            print(f"Error while creating tables: {error}")

    def insert_into_raw_tables(self, **kwargs):
        database = kwargs.get("database")
        data_tuple = kwargs.get("data_tuple")
        try:
            for file in os.listdir(RAW_FILE_PATH):
                if file.endswith('.sql'):
                    query = query_reader(os.path.join(RAW_FILE_PATH, file))
                    database.batch_execute_queries(query, data_tuple)
        except Exception as error:
            print(f"Error while inserting into raw tables: {error}")

    def insert_into_std_tables(self, database):
        try:
            for file in os.listdir(STD_FILE_PATH):
                if file.endswith('.sql'):
                    query = query_reader(os.path.join(STD_FILE_PATH, file))
                    database.execute_query(query)
        except Exception as error:
            print(f"Error while inserting into std tables: {error}")

    def insert_into_final_tables(self, database):
        try:
            for file in os.listdir(FINAL_FILE_PATH):
                if file.endswith('.sql'):
                    table_name = ' '.join(file.replace(".sql", '').split('_')[1:])
                    print(f"Inserting data into {table_name}")
                    query = query_reader(os.path.join(FINAL_FILE_PATH, file))
                    database.execute_query(query)
        except Exception as error:
            print(f"Error while inserting into final tables: {error}",)

    def get_total_data_count(self, database, *args):
        """Extract total count of data present"""
        pass

    def get_data_from_response(self, database, *args):
        """Extract data from the response"""
        pass

    def extract_data(self, database, *args, **kwargs) -> None:
        """Extract data from the source"""
        pass
