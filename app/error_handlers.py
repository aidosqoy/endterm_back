from flask import render_template

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html', error_code=404, error_message='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('error.html', error_code=500, error_message='Internal Server Error'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('error.html', error_code=403, error_message='Access Denied'), 403
