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
    data = get(ApiEndpoint.PENSIONS, id)
    if (not data):
        return None, 404

    return data, 200

def getAll():
    # For Migration: 
    #from backend.base import get, copyToMongo
    #data = get(ApiEndpoint.PENSIONS)
    #copyToMongo(data, ApiEndpoint.PENSIONS)
    # -----
    data = get(ApiEndpoint.PENSIONS)
    if (not data):
        return None, 404

    return data, 200

def create():
    response = post(ApiEndpoint.PENSIONS, request.json)
    if (not response['acknowledged']):
        return None, 400

    return response, 200

def update(id):
    response = updateItem(ApiEndpoint.PENSIONS, format(id), request.json)
    if (not response['acknowledged']):
        return None, 400

    return response, 200

def deleteId(id):
    response = delete(ApiEndpoint.PENSIONS, format(id))
    if (not response['acknowledged']):
        return None, 400
    return response, 200