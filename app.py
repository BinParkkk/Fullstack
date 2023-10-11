from flask import Flask, render_template, abort
from flask_restx import Api

from function.login import login
from jinja2 import TemplateNotFound

app = Flask(__name__)
authorizations = {
        "Authorization": {
                "type": "apiKey", 
                "in": "header", 
                "name": "Authorization",
                "description" : "Bearer JWT Authorization."
            },
        "appkey": {
            "type": "apiKey", 
            "in": "header", 
            "name": "appkey"
        }
}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/', defaults={'path' : ''})
@app.route('/<path:path>')
def index_path(path):
    try:
        return render_template('login.html')
    except TemplateNotFound:
        abort(404)

api = Api(app,
        version='0.0.1',
        title='Binpark Admin API',
        doc="/swagger",
        authorizations=authorizations
)

api.add_namespace(login, '/login') # 인증 관련 API

if __name__ == '__main__' :
    app.run(host = '127.0.0.1', port = '5000')

