import connexion
from flask_cors import CORS
# READ?? https://levelup.gitconnected.com/how-to-create-a-python-api-using-flask-connexion-4f3fc77e7f6e
app = connexion.FlaskApp(__name__, specification_dir='.')

CORS(app.app)
app.add_api('swagger.yaml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5678, debug=True)