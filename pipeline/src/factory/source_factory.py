from ..sources.api import ApiHandler
from ..sources.csv import CsvHandler

class SourceFactory:
    def select_handler(self, source_type: str = "api"):
        if source_type == "api":
            return ApiHandler()
        elif source_type == "csv":
            return CsvHandler()
        else:
            raise ValueError("Invalid Source")
