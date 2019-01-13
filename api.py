from flask import Flask
from flask_restful import Api
from controllers import epaController
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources=r'/epa/*')
api = Api(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/db/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

api.add_resource(epaController.epaController, '/epa')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
