from ..sources.api import ApiHandler
from ..sources.json_src import JSONHandler
from ..database.connection import PostgreSQLConnection

class SourceFactory:
    def select_handler(self, source_type: str = "api"):
        db = PostgreSQLConnection()
        if source_type == "api":
            return ApiHandler(db.connect())
        elif source_type == "json":
            return JSONHandler(db.connect())
        else:
            raise ValueError("Invalid Source")
