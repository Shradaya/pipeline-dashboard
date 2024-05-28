from app.dashapp.pages import leave, employee
# from dash import html, dcc, callback, Input, Output
from app.dashapp.pages.base_layout import base_layout
from dash_extensions.enrich import Input, Output, dcc, html, callback

def get_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

def get_application_page():
    @callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
    async def display_page(pathname):
        if pathname == '/dash/employee':
            emp_layout = await employee.layout()
            return base_layout(emp_layout)
        elif pathname == '/dash/':
            leave_layout = await leave.layout()
            return base_layout(leave_layout)
        else:
            return '404'