import dash
from flask.helpers import get_root_path
from app.dashapp.index import get_layout
from app.dashapp.index import get_application_page 
from .dashapp.callbacks import register_callbacks
from dash_extensions.enrich import DashProxy
    
    
def register_dashapps(app):
    """
    Register Dash apps with the Flask app
    """

    external_stylesheets = [
        'https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css'
    ]
    
    external_scripts = [
        "https://code.jquery.com/jquery-3.5.1.slim.min.js",
        "https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js",
        "https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.min.js",
    ]

    meta_viewport = [{
        "name": "viewport", 
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"
    }]

    dashapp = DashProxy(
        __name__,
        server = app,
        url_base_pathname = '/dash/',
        assets_folder = get_root_path(__name__) + 'app/static/', 
        meta_tags = meta_viewport, 
        external_scripts = external_scripts,
        external_stylesheets = external_stylesheets
    )
    dashapp.title = 'Leave Analysis'
    
    
    with app.app_context():
        dashapp.layout = get_layout() # # INITIALIZING LAYOUT
        register_callbacks(dashapp)
        get_application_page()
    return None
