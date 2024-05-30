from dash import dcc
from dash import html
from ..api_call import fetch_data
import dash_bootstrap_components as dbc
from ..constants import LEAVE_FILTER_OPTIONS_ENDPOINT
from ...utils.date_utils import convert_string_to_date

filter_options = {}

def get_body():
    """Get the body of the layout for our Dash SPA"""
    global filter_options
    projects = filter_options.get("projects", [])
    leave_types = filter_options.get("leave_types", [])
    departments = filter_options.get("departments", [])
    date_range_upper = convert_string_to_date(filter_options.get("date_range_upper"))
    date_range_lower = convert_string_to_date(filter_options.get("date_range_lower"))
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Label('Project', htmlFor='projects_dropdown'),
                dcc.Dropdown(
                    options=projects,
                    value=None,
                    placeholder="Select a Project ...",
                    id="projects_dropdown",
                    style={'width': '100%'}
                )
            ], width=2),
            dbc.Col([
                html.Label('Leave Type', htmlFor='leave_types_dropdown'),
                dcc.Dropdown(
                    options=leave_types,
                    value=None,
                    placeholder="Select a Leave Type ...",
                    id="leave_types_dropdown",
                    style={'width': '100%'}
                )
            ], width=2),
            dbc.Col([
                html.Label('Department', htmlFor='departments_dropdown'),
                dcc.Dropdown(
                    options=departments,
                    value=None,
                    placeholder="Select a Department ...",
                    id="departments_dropdown",
                    style={'width': '100%'}
                )
            ], width=2),
            dbc.Col([
                html.Label('Date Range', htmlFor='date_picker'),
                dcc.DatePickerRange(
                    min_date_allowed=date_range_lower,
                    max_date_allowed=date_range_upper,
                    id="date_picker",
                    style={'width': '100%'}
                )
            ], width=4)
        ], align='center'),
        html.Div(style={'height': '20px'})
    ])




def get_chart_row():
    """Create a row and column for our Plotly/Dash time series chart"""
    global filter_options
    fiscal_years = filter_options.get('fiscal_years')
    fiscal_year_options = [{'label': fy.get("label"), 'value': fy.get("value")} for fy in fiscal_years if fy.get("label") and fy.get("value")] if fiscal_years else []
    return html.Div([
        dbc.Row([
            dbc.Col(
                id="highest_leave_count",  
                children=[],
                width=6,
                style={'overflowX': 'auto', 'width': '700px'}
            ),
            dbc.Col(
                id="leave_applied_approved",  
                children=[],
                width=6
            )
        ]),
        dbc.Row([
            dbc.Col(
                id="leave_count_by_weekday",  
                children=[],
                width=6
            ),
            dbc.Col(
               children=[
                   dcc.Dropdown(
                       id='fiscal_year_dropdown',
                       options=fiscal_year_options,
                       placeholder="Choose Fiscal Year",
                       value=fiscal_year_options[0]['value'],
                       style={'width': '100%', 'marginBottom': '10px'}
                   ),
                   html.Div(id="leave_balance_table")  # Dedicated Div for the table
               ],
               width=6,
               style={'marginTop': '-150px', 'height': '700px'}  # Adjusted style
           )
        ])
    ])

def layout():
    """Function to get Dash's "HTML" layout"""
    global filter_options
    if not filter_options:
        filter_options = fetch_data(LEAVE_FILTER_OPTIONS_ENDPOINT)
    return dbc.Container(
        [
            get_body(), 
            get_chart_row(),
        ]
    )
