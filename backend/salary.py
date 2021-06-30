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
    response = insert(ApiEndpoint.SALARY, request.json)
    return response

def getAll():
    data = get(ApiEndpoint.SALARY)
    if (not data):
        return None, 404

    return data, 200

def getId(id):
    data = getById(ApiEndpoint.SALARY, format(id))

    if (not data):
        return None, 404

    return data, 200

def deleteId(id):
    delete(ApiEndpoint.SALARY, "Id = " +format(id))

    return None, 200
    
def getByYear(year):
    data = get(ApiEndpoint.SALARY, "Jahr = " + format(year))

    if (not data):
        return None, 404
    
    return data, 200