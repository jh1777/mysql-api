from backend.endpoint import ApiEndpoint
import pymysql
import pymysql.cursors
import connexion
import pendulum
from backend.baseMongo import get, post, getMongoResult
from connexion import request
app = connexion.App(__name__)
now = pendulum.now("Europe/Paris")

def create():
    response = post(ApiEndpoint.EXPENSES, request.json)
    if (not response.acknowledged):
        return None, 400

    return getMongoResult(response), 200

def getAll():
    data = get(ApiEndpoint.EXPENSES)
    if (not data):
        return None, 404

    return data, 200

def getId(id):
    data = get(ApiEndpoint.EXPENSES, id)
    if (not data):
        return None, 404

    return data, 200