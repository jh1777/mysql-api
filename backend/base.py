
import pymysql
from pymysql import Connection
import pymysql.cursors
import connexion
import pendulum
import json

from .endpoint import ApiEndpoint
now = pendulum.now("Europe/Paris")

app = connexion.App(__name__)
app.app.config.from_object("config.DevelopmentConfig")


def copyToMongo(items, apiType: ApiEndpoint):
    from backend.mapping import map
    from backend.baseMongo import getMongoCollection
    collection = getMongoCollection(apiType.name.lower())
    newresult = map(items)
    collection.insert_many(newresult)

def insert(apiType: ApiEndpoint, data: dict):
    values = ""
    columns = ""
    for key in data:
        columns += '`'+key+'`,'
        v = data[key]
        if (isinstance(v, str)):
            v = '"'+data[key]+'"'
        values += str(v)+','

    query = "INSERT INTO `" + apiType.value + "` (" + columns[:-1] + ") VALUES (" + values[:-1] + ");"
    app.app.logger.info(' [%s] insert: Endpoint=%s, Query=%s', now.to_iso8601_string(), apiType.name, query)
    connection = connectToDb()
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = query
            cursor.execute(sql)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
    

"""
Main entry point MQSQL
"""
def get(apiType: ApiEndpoint, whereClause: str = None):
    where = ''
    if whereClause != None:
        where = " WHERE " + whereClause

    query = "SELECT * FROM " + apiType.value + where
    app.app.logger.info(' [%s] get: Endpoint=%s, Query=%s', now.to_iso8601_string(), apiType.name, query)

    return queryDb(query, apiType)

def getById(apiType: ApiEndpoint, id: str):
    return get(apiType, 'Id = ' + id)

def delete(apiType: ApiEndpoint, whereClause: str):
    where = ''
    if whereClause != None:
        where = " WHERE " + whereClause

    query = "DELETE FROM " + apiType.value + where
    app.app.logger.info(' [%s] delete: Endpoint=%s, Query=%s', now.to_iso8601_string(), apiType.name, query)

    connection = connectToDb()
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = query
            cursor.execute(sql)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

def connectToDb() -> Connection:
    # Connect to the database
    db = pymysql.connect(host=app.app.config["DB_IP"],
                                user=app.app.config["DB_USERNAME"],
                                password=app.app.config["DB_PASSWORD"],
                                database=app.app.config["DB_NAME"],
                                cursorclass=pymysql.cursors.DictCursor)
    return db

def queryDb(queryString: str, apiType: ApiEndpoint):
    # Connect
    db = connectToDb()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute(queryString)
    data = cursor.fetchall()

    # disconnect from server
    db.close()

    # Migrate to Mongo
    #copyToMongo(data, apiType)

    return data
