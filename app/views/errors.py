"""
Error Handlers
"""

from flask import render_template

def register_error_handlers(app):
    """Register error handlers with the app"""
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template('train_error.html')
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('train_error.html')
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('train_error.html') 