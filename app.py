import connexion
from connexion.resolver import RestyResolver
#from flask_cors import CORS

application = connexion.App(__name__, specification_dir='openapi')

#api.add_api('swagger.yaml')
application.add_api(
    "swagger.yaml", resolver=RestyResolver("api"), strict_validation=False
)

# expose an app object for "flask run"
api = application.app

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5678, debug=True)