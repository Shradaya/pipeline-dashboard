
from dash import dash_table
import plotly.graph_objs as go
from app.database import get_conn
from dash.dependencies import State
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from dash.exceptions import PreventUpdate
from psycopg2.extras import RealDictCursor

from ..utils.sql_query import read_sql_query
from ..template.get_leave_count_per_weekday import LEAVE_COUNT_PER_WEEKDAY_QUERY
from ..template.get_late_applied_approved_leave_count import LATE_APPLIED_APPROVED_QUERY


def execute_sql_query(query, selected_project, leave_type, department, start_date, end_date):
    query, bind_params = read_sql_query(query, 
                                        selected_project = selected_project,
                                        leave_type = leave_type,
                                        department = department,
                                        start_date = start_date,
                                        end_date = end_date)
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory = RealDictCursor)
        cursor.execute(query, bind_params)
        leaves_per_week_day = cursor.fetchall()
    return leaves_per_week_day

def register_leave_callbacks(app):
    @app.callback(
        Output("leave_count_by_weekday", "children"),
        [
            Input("projects_dropdown", "value"),
            Input("leave_types_dropdown", "value"),
            Input("departments_dropdown", "value"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
         ]
    )
    def leaves_per_weekday_chart(selected_project, leave_type, department, start_date, end_date):
        day_counts = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        leaves_per_week_day = execute_sql_query(LEAVE_COUNT_PER_WEEKDAY_QUERY, 
                                                      selected_project, 
                                                      leave_type, 
                                                      department, 
                                                      start_date, 
                                                      end_date)

        # Update the counts based on the retrieved data
        for row in leaves_per_week_day:
            day_of_week = row['day_of_week']
            count = row['count']
            day_counts[day_of_week] = count

        # Convert the dictionary to lists for day_of_week and count
        day_of_week = list(day_counts.keys())
        count = list(day_counts.values())
        
        data = [
            go.Bar(
                x = day_of_week,
                y = count,
                marker = dict(color = 'blue'),
                name = 'Leave Count'
            )
        ]

        layout = go.Layout(
            title = "Leave Per Day Of Week",
            xaxis = dict(title = 'Day of Week'),
            yaxis = dict(title = 'Leave Count')
        )

        fig = {'data': data, 'layout': layout}
        return dcc.Graph(figure=fig)
    
    @app.callback(
        Output("leave_applied_approved", "children"),
        [
            Input("projects_dropdown", "value"),
            Input("leave_types_dropdown", "value"),
            Input("departments_dropdown", "value"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
         ]
    )
    def leaves_per_weekday_chart(selected_project, leave_type, department, start_date, end_date):
        leave_applied_approved = execute_sql_query(LATE_APPLIED_APPROVED_QUERY, 
                                                      selected_project, 
                                                      leave_type, 
                                                      department, 
                                                      start_date, 
                                                      end_date)
        
        # print(leave_applied_approved)
        if leave_applied_approved:
            data = leave_applied_approved[0]
            p_style = {'fontSize': 'small', 'color': 'grey', 'textAlign': 'center'}
            h3_style = {'textAlign': 'center'}
            width = 6
            table = html.Div([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.P("Total Count", style = p_style),
                        html.H3(data['total_count'], style = h3_style)
                    ]), width = width),
                    dbc.Col(html.Div([
                        html.P("Leave Applied Late", style = p_style),
                        html.H3(data['late_applied_leave'], style = h3_style)
                    ]), width = width)
                ]),
                dbc.Row([
                    dbc.Col(html.Div([
                        html.P("Leave Approved Late", style = p_style),
                        html.H3(data['late_approved_leave'], style = h3_style)
                    ]), width = width),
                    dbc.Col(html.Div([
                        html.P("Late Leave Unrejected", style = p_style),
                        html.H3(data['late_applied_leave_not_rejected'], style = h3_style)
                    ]), width = width)
                ])
            ])
            return table
        
