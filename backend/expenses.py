from backend.endpoint import ApiEndpoint
import pymysql
import pymysql.cursors
import connexion
import pendulum
from backend.baseMongo import get, post, delete, updateItem
from connexion import request
app = connexion.App(__name__)
now = pendulum.now("Europe/Paris")

def getId(id):
    data = get(ApiEndpoint.EXPENSES, id)
    if (not data):
        return None, 404

    return data, 200

def getAll():
    data = get(ApiEndpoint.EXPENSES)
    if (not data):
        return None, 404

    return data, 200

def create():
    response = post(ApiEndpoint.EXPENSES, request.json)
    if (not response['acknowledged']):
        return None, 400

    return response, 200

def update(id):
    response = updateItem(ApiEndpoint.EXPENSES, format(id), request.json)
    if (not response['acknowledged']):
        return None, 400

    return response, 200

def deleteId(id):
    response = delete(ApiEndpoint.EXPENSES, format(id))
    if (not response['acknowledged']):
        return None, 400
    return response, 200