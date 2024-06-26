import plotly.graph_objs as go
from ..api_call import fetch_data
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from ..constants import (LEAVE_COUNT_PER_WEEKDAY_ENDPOINT,
                            LATE_APPLIED_APPROVED_ENDPOINT,
                            LEAVE_HIGHEST_COUNT_ENDPOINT,
                            LEAVE_BALANCE_ENDPOINT)

def create_params(**kwargs):
    return {
        key: value for key, value in kwargs.items() if value is not None
    }

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
        params = create_params(
            selected_project=selected_project,
            leave_type=leave_type,
            department=department,
            start_date=start_date,
            end_date=end_date
        )
        leaves_per_week_day = fetch_data(LEAVE_COUNT_PER_WEEKDAY_ENDPOINT, params)

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
        params = create_params(
            selected_project=selected_project,
            leave_type=leave_type,
            department=department,
            start_date=start_date,
            end_date=end_date
        )
        leave_applied_approved = fetch_data(LATE_APPLIED_APPROVED_ENDPOINT, params)

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
        params = create_params(
            selected_project=selected_project,
            leave_type=leave_type,
            department=department,
            start_date=start_date,
            end_date=end_date
        )
        leave_count = fetch_data(LEAVE_HIGHEST_COUNT_ENDPOINT, params)
        color_combo = {
            "Leave Without Pay": "#FF0000",  # Red
            "Bereavement": "#008080",       # Teal
            "Sick": "#ADFF2F",              # GreenYellow
            "Paternity": "#FFFF00",         # Yellow
            "Compensatory": "#800080",      # Purple
            "Discretionary": "#FFD700",     # Gold (for consistency)
            "Menstruation": "#FFC0CB",      # Pink
            "Annual": "#0000FF"             # Blue
        }
        data = []
        leave_types = color_combo.keys()
        for leave_type in leave_types:
            x = []
            y = []
            for entry in leave_count:
                x.append(entry['name'])
                y.append(entry['leave_counts'].get(leave_type, 0))
            if any(y): 
                data.append(
                    go.Bar(
                        name=leave_type,
                        x=x,
                        y=y,
                        marker=dict(color=color_combo.get(leave_type, '#00FFFF'))
                    )
                )
        diagram_width = len(x) * 100
        layout = go.Layout(
            title = "Top Leave Counts by Type",
            title_x = 0.5,
            margin = dict(t = 30),
            xaxis = dict(
                title = 'Employee',
                tickmode = 'linear',
                tickangle = -15,
                automargin = True
            ),
            yaxis = dict(title = 'Leave Count'),
            height = 350,
            width = diagram_width if diagram_width > 600 else 600,
            barmode = 'stack',  # This enables stacking
            legend=dict(
                x=0,
                y=1.1,
                orientation='h'
            )
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
        params = create_params(
            selected_project= selected_project,
            leave_type= leave_type,
            department= department,
            fiscal_year = fiscal_year
        )
        leave_balance = fetch_data(LEAVE_BALANCE_ENDPOINT, params)

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
