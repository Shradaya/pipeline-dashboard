from app.dashapp.pages import leave, employee
from dash import html, dcc, callback, Input, Output
from app.dashapp.pages.base_layout import base_layout

def get_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

def get_application_page():
    @callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/dash/employee':
            return base_layout(employee.layout())
        elif pathname == '/dash/':
            return base_layout(leave.layout())
        else:
            return '404'