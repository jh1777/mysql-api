from backend.endpoint import ApiEndpoint
import pymysql
import pymysql.cursors
import connexion
import pendulum
from backend.baseMongo import get, post, delete, updateItem
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

    for item in data:
        padding = ''
        if item['Monat']<10:
            padding = '0'
        item['_sortKey'] = int(str(item['Jahr'])+padding+str(item['Monat']))
    if (not data):
        return None, 404

    return data, 200

def getId(id):
    data = get(ApiEndpoint.SALARY, format(id))
    if (not data):
        return None, 404

    return data, 200

def update(id):
    response = updateItem(ApiEndpoint.SALARY, format(id), request.json)
    if (not response['acknowledged']):
        return None, 400

    return response, 200

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