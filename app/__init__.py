from flask import Flask
def create_app(config_name='default'):
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Load configuration
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
    else:
        app.config['TESTING'] = False
    
    app.config['SECRET_KEY'] = 'osdag-structural-dashboard-2026'
    
    # Register routes
    from .main import main_bp
    app.register_blueprint(main_bp)
    
    return app

__version__ = '1.0.0'
__author__ = 'Suman Kumar'
