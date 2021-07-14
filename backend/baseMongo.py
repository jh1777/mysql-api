
from pymongo import collection
from pymongo.results import DeleteResult, InsertManyResult, UpdateResult
from backend.endpoint import ApiEndpoint
from bson.objectid import ObjectId
import connexion
import pendulum
now = pendulum.now("Europe/Paris")
from backend.mapping import map

app = connexion.App(__name__)
app.app.config.from_object("config.DevelopmentConfig")

from backend.decimalCodec import DecimalCodec
from decimal import Decimal
from bson.codec_options import CodecOptions, TypeRegistry
from pymongo import MongoClient

# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = app.app.config["MONGO"]

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
from pymongo import MongoClient
client = MongoClient(CONNECTION_STRING)
app.app.logger.info('Connecting to Mongo DB "finances"')

# Create the database for our example (we will use the same database throughout the tutorial
db = client['finances']
decimal_codec = DecimalCodec()
type_registry = TypeRegistry([decimal_codec])
codec_options = CodecOptions(type_registry=type_registry)


def getMongoCollection(name: str):
    collection = db.get_collection(name, codec_options=codec_options)
    return collection

def get(api: ApiEndpoint, id: str = None, filter: dict = None) -> list:
    collection = getMongoCollection(api.name.lower())
    app.app.logger.info('Getting data from Mongo DB collection "%s"', api.name.lower())

    if id != None:
        if ObjectId.is_valid(id):
            data = collection.find_one({"_id": ObjectId(id) })
            return data
        else:
            raise ValueError('No ObjectID was found - nothing to query!')

    if filter != None:
        data = list(collection.find(filter))
        return data

    data = list(collection.find())
    return data

def endeFilter(item):
    if "Ende" in item and item['Ende'] != None:
        return pendulum.instance(item['Ende'], "Europe/Paris") > now
    return True

def getActiveOnly(_api: ApiEndpoint, _id: str = None, _filter: dict = None) -> list:
    data = get(_api, _id, _filter)
    filteredData = filter(endeFilter, data)
    return list(filteredData)

def post(api: ApiEndpoint, items) -> dict:
    collection = getMongoCollection(api.name.lower())
    app.app.logger.info('Inserting data to Mongo DB collection "%s"', api.name.lower())
    docs = map(items)
    # Add a system creation date
    for doc in docs:
        doc['_modified']=now
        doc['_created']=now
    result = collection.insert_many(docs)
    # Create API response
    return mapMongoResultObject(result)

def delete(api: ApiEndpoint, id: str) -> dict:
    collection = getMongoCollection(api.name.lower())
    app.app.logger.info('Deleting item %s from Mongo DB collection "%s"', id, api.name.lower())
    response = collection.delete_one({"_id": ObjectId(id) })
    # Create API response
    return mapMongoResultObject(response)

def updateItem(api: ApiEndpoint, id: str, updates: dict) -> dict:
    collection = getMongoCollection(api.name.lower())
    app.app.logger.info('Updating item %s in Mongo DB collection "%s"', id, api.name.lower())
    docs = map([updates])
    doc = docs[0]
    # Add a system modification date 
    doc['_modified']=now
    response = collection.update_one({"_id": ObjectId(id) }, {"$set": doc }, upsert=False)
    # Create API response
    return mapMongoResultObject(response)


def mapMongoResultObject(response) -> dict:
    result: dict
    if isinstance(response, InsertManyResult):
        ids = []
        for id in response.inserted_ids:
            ids.append(str(id))
        result = { "acknowledged": response.acknowledged, "inserted_ids": ', '.join(ids) }

    if isinstance(response, DeleteResult):
        result = { "acknowledged": response.acknowledged, "deleted_count": response.deleted_count }

    if isinstance(response, UpdateResult):
        result = { "acknowledged": response.acknowledged, "matched_count": response.matched_count, "modified_count": response.modified_count, "upserted_id": response.upserted_id }

    app.app.logger.info('%s from Mongo DB operation = %s', response.__class__.__name__, result)
    return result

"""
Migration of a Doc: For later Usage (untested)
"""
def documentMigration(api: ApiEndpoint, updates: dict):
    collection = getMongoCollection(api.name.lower())
    docs = collection.find()
    ## DO SOMETHING WITH updates AND docs

    result = []
    for doc in docs:
        docresult = collection.update_one({"_id": ObjectId(id) }, {"$set": doc }, upsert=False)
        result.append(mapMongoResultObject(docresult))

    ## ----
    return result