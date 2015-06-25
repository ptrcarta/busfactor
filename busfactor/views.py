from flask import render_template

def register_views(app):
    @app.route("/")
    def index():
        return render_template('index.html')
