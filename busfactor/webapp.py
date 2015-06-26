from flask import Flask
from views import register_views

app = Flask(__name__)
register_views(app)

if __name__ == '__main__': app.run(debug=True)
