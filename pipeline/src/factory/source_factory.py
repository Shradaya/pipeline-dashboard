from ..sources.api import ApiHandler
from ..sources.csv import CsvHandler
from ..database.connection import PostgreSQLConnection

class SourceFactory:
    def select_handler(self, source_type: str = "api"):
        db = PostgreSQLConnection()
        if source_type == "api":
            return ApiHandler(db.connect())
        elif source_type == "csv":
            return CsvHandler(db.connect())
        else:
            raise ValueError("Invalid Source")
