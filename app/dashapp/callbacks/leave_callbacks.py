import requests
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from ...constants import (LEAVE_COUNT_PER_WEEKDAY_ENDPOINT,
                            LATE_APPLIED_APPROVED_ENDPOINT,
                            HIGHEST_LEAVE_COUNT_ENDPOINT,
                            LEAVE_BALANCE_ENDPOINT)

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
        params = {
            'selected_project': selected_project,
            'leave_type': leave_type,
            'department': department,
            'start_date': start_date,
            'end_date': end_date
        }
        try:
            response = requests.get(LEAVE_COUNT_PER_WEEKDAY_ENDPOINT, params=params)
        except requests.RequestException as e:
            print(f"Request Failed: {e}")
        except ValueError as e:
            print(f"Invalid JSON response: {e}")
        leaves_per_week_day = response.json()

        day_of_week = leaves_per_week_day.get('day_of_week')
        count = leaves_per_week_day.get('count')

        data = [
            go.Bar(
                x=day_of_week,
                y=count,
                marker=dict(color='blue'),
                name='Leave Count'
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
    def leave_metrics_chart(selected_project, leave_type, department, start_date, end_date):
        params = {
            'selected_project': selected_project,
            'leave_type': leave_type,
            'department': department,
            'start_date': start_date,
            'end_date': end_date
        }
        try:
            response = requests.get(LATE_APPLIED_APPROVED_ENDPOINT, params=params)
            response.raise_for_status()
            leave_applied_approved = response.json()
        except requests.RequestException as e:
            print(f"Request Failed: {e}")
            return html.Div("Error fetching data.")

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
        params = {
            'selected_project': selected_project,
            'leave_type': leave_type,
            'department': department,
            'start_date': start_date,
            'end_date': end_date
        }
        try:
            response = requests.get(HIGHEST_LEAVE_COUNT_ENDPOINT, params=params)
            response.raise_for_status()
            leave_applied_approved = response.json()
        except requests.RequestException as e:
            print(f"Request Failed: {e}")
            return html.Div("Error fetching data.")

        # Extract names and leave counts
        names = leave_applied_approved.get("names")
        leave_counts = leave_applied_approved.get("leave_counts")

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
                tickangle=-15,
                automargin=True
            ),
            yaxis=dict(title='Leave Count'),
            height=350,
            width=diagram_width if diagram_width > 600 else 600, 
            xaxis_type='category'
        )

        fig = {'data': data, 'layout': layout}
        return dcc.Graph(figure=fig, config={'staticPlot': False})
    
    @app.callback(
        Output("leave_balance_table", "children"),
        [
            Input("projects_dropdown", "value"),
            Input("leave_types_dropdown", "value"),
            Input("departments_dropdown", "value"),
            Input("fiscal_year_dropdown", "value")
        ]
    )
    def leave_balance_table(selected_project, leave_type, department, fiscal_year):
        params = {
            'selected_project': selected_project,
            'leave_type': leave_type,
            'department': department,
            'fiscal_year': fiscal_year
        }
        try:
            response = requests.get(LEAVE_BALANCE_ENDPOINT, params=params, timeout = 30)
            response.raise_for_status()
            leave_balance = response.json()
        except requests.RequestException as e:
            print(f"Request Failed: {e}")
            return html.Div("Error fetching data")
        

        table_header = [
            html.Thead(html.Tr([html.Th("Full Name"), html.Th("Leave Type"), html.Th("Credits"), html.Th("Taken"), html.Th("Available")]), 
                       style={'position': 'sticky', 'top': 0, 'background': 'white', 'zIndex': 1})
        ]
        table_body = [html.Tr([
            html.Td(entry['full_name']),
            html.Td(entry['leave_type_name']),
            html.Td(entry['available_leave_count']),
            html.Td(entry['leaves_taken']),
            html.Td(entry['remaining_leave_count'])
        ]) for entry in leave_balance]

        table = dbc.Table(table_header + [html.Tbody(table_body)], bordered=True, hover=True, responsive=True, striped=True)
        scrollable_table = html.Div(table, style={'overflowY': 'auto', 'height': '500px'})

        return scrollable_table
