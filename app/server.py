from flask import Flask
from flask_restful import Api
from app.controllers import andaluhController
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/docs'
API_URL = 'https://raw.githubusercontent.com/andalugeeks/andaluh-api/master/swagger.json'

app = Flask(__name__)

# Add Swagger UI at basepah
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Add EPA API at /epa path
api = Api(app)
cors = CORS(app, resources=r'/epa/*')
api.add_resource(andaluhController.andaluhController, '/epa')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
