import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.environ.get("FLASK_API_ENDPOINT")
LEAVE_COUNT_PER_WEEKDAY_ENDPOINT = f"{API_BASE_URL}/leave/per-weekday"
LATE_APPLIED_APPROVED_ENDPOINT = f"{API_BASE_URL}/leave/metrics"
LEAVE_HIGHEST_COUNT_ENDPOINT = f"{API_BASE_URL}/leave/highest-count"
LEAVE_BALANCE_ENDPOINT = f"{API_BASE_URL}/leave/balance"

LEAVE_FILTER_OPTIONS_ENDPOINT = f"{API_BASE_URL}/leave/filter-options"
