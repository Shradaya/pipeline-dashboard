import os
import json
import requests
from ..config import BEARER_TOKEN, API_ENDPOINT
from .utils import escape_single_quotes_in_dict
from ..interfaces.source_interface import SourceInterface

class ApiHandler(SourceInterface):
    def __init__(self, database):
        self.db = database 
    
    def get_total_data_count(self, response):
        return response.get("meta", {}).get("total", len(self.get_data_from_response(response)))

    def get_data_from_response(self, response):
        return response['data']
    
    def create_tables(self, _ = None):
        return super().create_tables(self.db)
   
    def extract_data(self, *args, fetch_type: str = "all") -> dict:
        file_path = './response.json'
        if os.path.isfile(file_path):
            with open(file_path) as f:
                response = json.loads(f.read())
            return response
        params = {
            "startDate": args[0],
            "endDate": args[1],
            "size": args[2],
            "page": args[3],
            "fetchType": fetch_type,
            "roleType": "issuer"
        }

        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }

        response = requests.get(API_ENDPOINT, params = params, headers = headers)
        if response.status_code == 200:
            print("Request was successful!")
            return response.json()
        else:
            print("Error:", response.status_code)
        

    def insert_into_raw_tables(self, **kwargs) -> None:
        tuples_to_insert = []
        raw_datas = kwargs["raw_data_set"]
        for raw_data in raw_datas:
            allocations = raw_data.get('allocations')

            tuples_to_insert.append(
                (
                    str(raw_data.get('id', '')),
                    str(raw_data.get('userId', '')),
                    str(raw_data.get('empId', '')),
                    str(raw_data.get('teamManagerId', '')),
                    str(raw_data.get('designationId', '')),
                    str(raw_data.get('designationName', '')),
                    str(raw_data.get('firstName', '')),
                    str(raw_data.get('middleName', '')),
                    str(raw_data.get('lastName', '')),
                    str(raw_data.get('email', '')),
                    str(raw_data.get('isHr', '')),
                    str(raw_data.get('isSupervisor', '')),
                    json.dumps([escape_single_quotes_in_dict(allocation) for allocation in raw_data.get('allocations')]) if allocations else None,
                    str(raw_data.get('leaveIssuerId', '')),
                    str(raw_data.get('currentLeaveIssuerId', '')),
                    str(raw_data.get('leaveIssuerFirstName', '')),
                    str(raw_data.get('leaveIssuerLastName', '')),
                    str(raw_data.get('currentLeaveIssuerEmail', '')),
                    str(raw_data.get('departmentDescription', '')),
                    str(raw_data.get('startDate', '')),
                    str(raw_data.get('endDate', '')),
                    str(raw_data.get('leaveDays', '')),
                    str(raw_data.get('reason', '')),
                    str(raw_data.get('status', '')),
                    str(raw_data.get('remarks', '')),
                    str(raw_data.get('leaveTypeId', '')),
                    str(raw_data.get('leaveTypeName', '')),
                    str(raw_data.get('defaultDays', '')),
                    str(raw_data.get('transferableDays', '')),
                    str(raw_data.get('isConsecutive', '')),
                    str(raw_data.get('fiscalId', '')),
                    str(raw_data.get('fiscalStartDate', '')),
                    str(raw_data.get('fiscalEndDate', '')),
                    str(raw_data.get('fiscalIsCurrent', '')),
                    str(raw_data.get('createdAt', '')),
                    str(raw_data.get('updatedAt', '')),
                    str(raw_data.get('isConverted', '')),
                )
            )
        return super().insert_into_raw_tables(database = self.db, data_tuple = tuples_to_insert)

    def insert_into_std_tables(self, _ = None) -> None:
        return super().insert_into_std_tables(self.db)
    
    def insert_into_final_tables(self, _ = None) -> None:
        return super().insert_into_final_tables(self.db)
