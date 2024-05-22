import plotly.graph_objs as go
from app.database import get_conn
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from psycopg2.extras import RealDictCursor

from ..utils.sql_query import read_sql_query
from ..template.leave_page.get_highest_leave_count import HIGHEST_LEAVE_COUNT_QUERY
from ..template.leave_page.get_leave_count_per_weekday import LEAVE_COUNT_PER_WEEKDAY_QUERY
from ..template.leave_page.get_late_applied_approved_leave_count import LATE_APPLIED_APPROVED_QUERY


def execute_sql_query(query, selected_project, leave_type, department, start_date, end_date):
    query, bind_params = read_sql_query(query,
                                        selected_project=selected_project,
                                        leave_type=leave_type,
                                        department=department,
                                        start_date=start_date,
                                        end_date=end_date)
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
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
        day_counts = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0}

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
                x=day_of_week,
                y=count,
                marker=dict(color='blue'),
                name='Leave Count',
            )
        ]

        layout = go.Layout(
            title="Leave Per Day Of Week",
            title_x=0.5, 
            margin=dict(t=30), 
            xaxis=dict(
                title='Day Of Week', 
                tickmode='linear',
                tickangle=0,
                automargin=True
            ),
            yaxis=dict(title='Leave Count'),
            height=350,
            width=500,
            xaxis_type='category'
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

        if leave_applied_approved:
            data = leave_applied_approved[0]
            p_style = {'fontSize': 'small',
                       'color': 'grey', 
                       'textAlign': 'center'}
            h3_style = {'textAlign': 'center'}
            table = html.Div([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.P("Total Count", style=p_style),
                        html.H3(data['total_count'], style=h3_style)
                    ])),
                    dbc.Col(html.Div([
                        html.P("Leave Applied Late", style=p_style),
                        html.H3(data['late_applied_leave'], style=h3_style)
                    ]))
                ]),
                dbc.Row([
                    dbc.Col(html.Div([
                        html.P("Leave Approved Late", style=p_style),
                        html.H3(data['late_approved_leave'], style=h3_style)
                    ])),
                    dbc.Col(html.Div([
                        html.P("Late Leave Unrejected", style=p_style),
                        html.H3(
                            data['late_applied_leave_not_rejected'], style=h3_style)
                    ]))
                ])
            ])
            return table
    
    @app.callback(
        Output("highest_leave_count", "children"),
        [
            Input("projects_dropdown", "value"),
            Input("leave_types_dropdown", "value"),
            Input("departments_dropdown", "value"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date")
        ]
    )
    def highest_leave_count_chart(selected_project, leave_type, department, start_date, end_date):
        leave_applied_approved = execute_sql_query(HIGHEST_LEAVE_COUNT_QUERY,
                                                selected_project,
                                                leave_type,
                                                department,
                                                start_date,
                                                end_date)

        # Extract names and leave counts
        names = [entry['full_name'] for entry in leave_applied_approved]
        leave_counts = [entry['leave_count'] for entry in leave_applied_approved]

        # Create the bar graph
        data = [
            go.Bar(
                x=names,
                y=leave_counts,
                marker=dict(color='blue'),
                name='Leave Count'
            )
        ]
        diagram_width = len(names) * 100

        layout = go.Layout(
            title="Top Leave Counts",
            title_x=0.5, 
            margin=dict(t=30), 
            xaxis=dict(
                title='Employee', 
                tickmode='linear',
                tickangle=0,
                automargin=True
            ),
            yaxis=dict(title='Leave Count'),
            height=350,
            width=diagram_width if diagram_width > 600 else 600, 
            xaxis_type='category'
        )

        fig = {'data': data, 'layout': layout}
        return dcc.Graph(figure=fig, config={'staticPlot': False})
