from backend.endpoint import ApiEndpoint
import pymysql
import pymysql.cursors
import connexion
import pendulum
import json
from backend.baseMongo import get, post, delete
from connexion import request
app = connexion.App(__name__)
now = pendulum.now("Europe/Paris")

def create():
    response = post(ApiEndpoint.SALARY, request.json)
    if (not response['acknowledged']):
        return None, 400

    return response, 200

def getAll():
    data = get(ApiEndpoint.SALARY)
    if (not data):
        return None, 404

    return data, 200

def getId(id):
    data = get(ApiEndpoint.SALARY, id)
    if (not data):
        return None, 404

    return data, 200

def deleteId(id):
    response = delete(ApiEndpoint.SALARY, format(id))
    if (not response['acknowledged']):
        return None, 400
    return response, 200
    
def getByYear(year):
    data = get(ApiEndpoint.SALARY, None, {"Jahr": year })
    if (not data):
        return None, 404
    
    return data, 200