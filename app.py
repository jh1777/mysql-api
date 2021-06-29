import connexion
#from flask_cors import CORS

api = connexion.FlaskApp(__name__, specification_dir='.')

#CORS(api.app)
api.add_api('swagger.yaml')

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5678, debug=True)