from backend.endpoint import ApiEndpoint
import pymysql
import pymysql.cursors
import connexion
import pendulum
from backend.base import get, getById, insert, delete
from connexion import request
app = connexion.App(__name__)
now = pendulum.now("Europe/Paris")

def create():
    response = insert(ApiEndpoint.EXPENSES, request.json)
    return response

def getAll():
    data = get(ApiEndpoint.EXPENSES)
    if (not data):
        return None, 404

    return data, 200