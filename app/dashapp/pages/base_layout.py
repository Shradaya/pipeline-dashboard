from dash import html
import dash_bootstrap_components as dbc 

def base_layout(page_content):
    """Function to get Dash's "HTML" layout"""
    return html.Div([
        dbc.NavbarSimple(
            brand = "Leave Analysis Home",
            brand_href = "/",
            color = "dark",
            dark = True
        ),
        html.Main(page_content, className="app-content")
    ])
