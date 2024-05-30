from flask import request
from ...base import api_router_v1
from .controller import leaves_per_weekday, leave_metrics, highest_leave_count, leave_balance_controller, get_filter_options

@api_router_v1.route('/leave/per-weekday')
def leave_per_weekday_route():
    selected_project = request.args.get('selected_project', None)
    leave_type = request.args.get('leave_type', None)
    department = request.args.get('department', None)
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    return leaves_per_weekday(selected_project, leave_type, department, start_date, end_date)

@api_router_v1.route('/leave/metrics')
def leave_metrics_route():
    selected_project = request.args.get('selected_project', None)
    leave_type = request.args.get('leave_type', None)
    department = request.args.get('department', None)
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    return leave_metrics(selected_project, leave_type, department, start_date, end_date)

@api_router_v1.route('/leave/highest-count')
def highest_leave_count_route():
    selected_project = request.args.get('selected_project', None)
    leave_type = request.args.get('leave_type', None)
    department = request.args.get('department', None)
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    return highest_leave_count(selected_project, leave_type, department, start_date, end_date)

@api_router_v1.route('/leave/balance')
def leave_balance_route():
    selected_project = request.args.get('selected_project', None)
    leave_type = request.args.get('leave_type', None)
    department = request.args.get('department', None)
    fiscal_year = request.args.get('fiscal_year', None)
    return leave_balance_controller(selected_project, leave_type, department, fiscal_year)

@api_router_v1.route('/leave/filter-options')
def leave_filter_options_route():
    return get_filter_options()