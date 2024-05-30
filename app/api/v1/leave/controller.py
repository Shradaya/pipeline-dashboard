from ..template.leave_page.get_leave_balance import LEAVE_BALANCE_QUERY
from ..template.leave_page.get_highest_leave_count import HIGHEST_LEAVE_COUNT_QUERY
from ..template.leave_page.get_leave_count_per_weekday import LEAVE_COUNT_PER_WEEKDAY_QUERY
from ..template.leave_page.get_late_applied_approved_leave_count import LATE_APPLIED_APPROVED_QUERY

from .services import execute_sql_query
from ..template.leave_page.filter_options import (PROJECT_OPTIONS, LEAVE_TYPE_OPTIONS, DEPARTMENT_OPTIONS, 
                                                  DATE_RANGE_OPTIONS, FISCAL_YEAR_OPTIONS)
from ....utils.date_utils import convert_date_to_string

def get_filter_options():
    projects = execute_sql_query(PROJECT_OPTIONS)
    leave_types = execute_sql_query(LEAVE_TYPE_OPTIONS)
    departments = execute_sql_query(DEPARTMENT_OPTIONS)
    date_range = execute_sql_query(DATE_RANGE_OPTIONS)
    fiscal_years = execute_sql_query(FISCAL_YEAR_OPTIONS)
    return  {
        "projects": projects,
        "leave_types": leave_types,
        "departments": departments,
        "date_range_lower": convert_date_to_string(date_range[0]['lower_bound'] if date_range else None),
        "date_range_upper": convert_date_to_string(date_range[0]['upper_bound'] if date_range else None),
        "fiscal_years": fiscal_years
    }


def leaves_per_weekday(selected_project, leave_type, department, start_date, end_date):
    day_counts = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0}

    leaves_per_week_day = execute_sql_query(LEAVE_COUNT_PER_WEEKDAY_QUERY,
                                            selected_project = selected_project,
                                            leave_type = leave_type,
                                            department = department,
                                            start_date = start_date,
                                            end_date = end_date)
    # Update the counts based on the retrieved data
    for row in leaves_per_week_day:
        day_of_week = row['day_of_week']
        count = row['count']
        day_counts[day_of_week] = count

    # Convert the dictionary to lists for day_of_week and count
    day_of_week = list(day_counts.keys())
    count = list(day_counts.values())
    
    return {
        "day_of_week": day_of_week,
        "count": count
    }
    

def leave_metrics(selected_project, leave_type, department, start_date, end_date):
    leave_metrics = execute_sql_query(LATE_APPLIED_APPROVED_QUERY,
                                                selected_project = selected_project,
                                                leave_type = leave_type,
                                                department = department,
                                                start_date = start_date,
                                                end_date = end_date)
    return leave_metrics

def highest_leave_count(selected_project, leave_type, department, start_date, end_date):
    leave_counts = execute_sql_query(HIGHEST_LEAVE_COUNT_QUERY,
                                               selected_project=selected_project,
                                               leave_type=leave_type,
                                               department=department,
                                               start_date=start_date,
                                               end_date=end_date)

    # Process results to group by name and aggregate leave counts by type
    results = {}
    for entry in leave_counts:
        full_name = entry['full_name']
        leave_type = entry['leave_type_name']
        count = entry['leave_count']

        if full_name not in results:
            results[full_name] = {}

        results[full_name][leave_type] = count

    formatted_results = []
    for name, leave_counts in results.items():
        formatted_results.append({
            "name": name,
            "leave_counts": leave_counts
        })

    return formatted_results
    
def leave_balance_controller(selected_project, leave_type, department, fiscal_year):
    leave_balance = execute_sql_query(LEAVE_BALANCE_QUERY,
                                    selected_project = selected_project,
                                    leave_type = leave_type,
                                    department = department,
                                    fiscal_year = fiscal_year)
    return leave_balance