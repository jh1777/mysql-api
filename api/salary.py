import pymysql
import pymysql.cursors
import connexion

from api.base import queryDb

def create():
    return  "Created"

def getAll():
    return "Get All entries"

def getById(id):

    data = queryDb("select * from Gehalt where Id = " + format(id))

    if (not data):
        return None, 404

    return data, 200
    
def getByYear(year):

    data = queryDb("select * from Gehalt where Jahr = " + format(year))

    if (not data):
        return None, 404
    
    return data, 200