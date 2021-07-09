from backend.endpoint import ApiEndpoint
import pymysql
import pymysql.cursors
import connexion
import pendulum
from backend.baseMongo import get
from backend.base import getById, insert, delete
from connexion import request
app = connexion.App(__name__)
now = pendulum.now("Europe/Paris")

def create():
    #response = insert(ApiEndpoint.SALARY, request.json)
    #return response
    return None, 200

def getAll():
    # OLD data = get(ApiEndpoint.SALARY)
    from backend.baseMongo import get
    data = get(ApiEndpoint.SALARY)
    if (not data):
        return None, 404

    return data, 200

def getId(id):
    from backend.baseMongo import get
    data = get(ApiEndpoint.SALARY, id)
    if (not data):
        return None, 404

    return data, 200

def deleteId(id):
    #delete(ApiEndpoint.SALARY, "Id = " +format(id))

    return None, 200
    
def getByYear(year):
    #data = get(ApiEndpoint.SALARY, "Jahr = " + format(year))
    data = get(ApiEndpoint.SALARY, None, {"Jahr": year })
    if (not data):
        return None, 404
    
    return data, 200