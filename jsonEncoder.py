from bson.objectid import ObjectId
from connexion.apps.flask_app import FlaskJSONEncoder


class CustomJSONEncoder(FlaskJSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        return super().default(o)