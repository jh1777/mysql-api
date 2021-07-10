
from pymongo import collection
from pymongo.results import DeleteResult, InsertManyResult
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

# Create the database for our example (we will use the same database throughout the tutorial
db = client['finances']
decimal_codec = DecimalCodec()
type_registry = TypeRegistry([decimal_codec])
codec_options = CodecOptions(type_registry=type_registry)


def getMongoCollection(name: str):
    collection = db.get_collection(name, codec_options=codec_options)
    return collection

def get(api: ApiEndpoint, id: str = None, filter: dict = None):
    collection = getMongoCollection(api.name.lower())
    if id != None:
        data = collection.find_one({"_id": ObjectId(id) })
        return data

    if filter != None:
        data = list(collection.find(filter))
        return data

    data = list(collection.find())
    return data

def post(api: ApiEndpoint, items) -> InsertManyResult:
    collection = getMongoCollection(api.name.lower())
    docs = map(items)
    # Add a system creation date
    for doc in docs:
        doc['_created']=now
    result = collection.insert_many(docs)
    # Create API response
    return getMongoResult(result)

def delete(api: ApiEndpoint, id: str) -> dict:
    collection = getMongoCollection(api.name.lower())
    response = collection.delete_one({"_id": ObjectId(id) })
    # Create API response
    result = { "acknowledged": response.acknowledged, "deleted_count": response.deleted_count }
    return result

def updateItem(api: ApiEndpoint, id: str, updates: dict):
    collection = getMongoCollection(api.name.lower())
    docs = map([updates])
    doc = docs[0]
    # Add a system modification date 
    # TODO: bug .. always 1
    doc['_modified']=now
    if '_modifiedCount' in doc:
        doc['_modifiedCount'] = doc['_modifiedCount'] + 1
    else:
        doc['_modifiedCount'] = 1

    response = collection.update_one({"_id": ObjectId(id) }, {"$set": doc }, upsert=False)
    # Create API response
    result = { "acknowledged": response.acknowledged, "matched_count": response.matched_count, "modified_count": response.modified_count, "upserted_id": response.upserted_id, "_id": id }
    return result

def getMongoResult(result: InsertManyResult) -> dict:
    ids = []
    for id in result.inserted_ids:
        ids.append(str(id))
    return { "acknowledged": result.acknowledged, "inserted_ids": ', '.join(ids) }