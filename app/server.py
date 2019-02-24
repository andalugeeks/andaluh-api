from flask import Flask
from flask_restful import Api
from controllers import andaluhController
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources=r'/epa/*')
api = Api(app)

api.add_resource(andaluhController.andaluhController, '/epa')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
