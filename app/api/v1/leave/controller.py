from ..template.leave_page.get_leave_balance import LEAVE_BALANCE_QUERY
from ..template.leave_page.get_highest_leave_count import HIGHEST_LEAVE_COUNT_QUERY
from ..template.leave_page.get_leave_count_per_weekday import LEAVE_COUNT_PER_WEEKDAY_QUERY
from ..template.leave_page.get_late_applied_approved_leave_count import LATE_APPLIED_APPROVED_QUERY

from .services import execute_sql_query

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
    leave_applied_approved = execute_sql_query(HIGHEST_LEAVE_COUNT_QUERY,
                                            selected_project = selected_project,
                                            leave_type = leave_type,
                                            department = department,
                                            start_date = start_date,
                                            end_date = end_date)

    # Extract names and leave counts
    names = [entry['full_name'] for entry in leave_applied_approved]
    leave_counts = [entry['leave_count'] for entry in leave_applied_approved]
    
    return {
        "names": names,
        "leave_counts": leave_counts
    }
    
def leave_balance_controller(selected_project, leave_type, department, fiscal_year):
    leave_balance = execute_sql_query(LEAVE_BALANCE_QUERY,
                                    selected_project = selected_project,
                                    leave_type = leave_type,
                                    department = department,
                                    fiscal_year = fiscal_year)
    return leave_balance