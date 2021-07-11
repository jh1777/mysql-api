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
    data = get(ApiEndpoint.INSURANCES, id)
    if (not data):
        return None, 404

    return data, 200

def getAll():
    # For Migration: 
    #from backend.base import get, copyToMongo
    #data = get(ApiEndpoint.INSURANCES)
    #copyToMongo(data, ApiEndpoint.INSURANCES)
    # -----
    data = get(ApiEndpoint.INSURANCES)
    if (not data):
        return None, 404

    return data, 200

def create():
    response = post(ApiEndpoint.INSURANCES, request.json)
    if (not response['acknowledged']):
        return None, 400

    return response, 200

def update(id):
    response = updateItem(ApiEndpoint.INSURANCES, format(id), request.json)
    if (not response['acknowledged']):
        return None, 400

    return response, 200

def deleteId(id):
    response = delete(ApiEndpoint.INSURANCES, format(id))
    if (not response['acknowledged']):
        return None, 400
    return response, 200