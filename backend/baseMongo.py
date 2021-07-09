
import re
from pymongo import collection
from pymongo.results import InsertManyResult
from backend.endpoint import ApiEndpoint
from bson.objectid import ObjectId
import connexion
import pendulum
now = pendulum.now("Europe/Paris")

app = connexion.App(__name__)
app.app.config.from_object("config.DevelopmentConfig")

def getMongoCollection(name: str):
    from pymongo import MongoClient
    from backend.decimalCodec import DecimalCodec
    from decimal import Decimal
    from bson.codec_options import CodecOptions, TypeRegistry

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = app.app.config["MONGO"]

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    dbname = client['finances']
    decimal_codec = DecimalCodec()
    type_registry = TypeRegistry([decimal_codec])
    codec_options = CodecOptions(type_registry=type_registry)
    collection = dbname.get_collection(name, codec_options=codec_options)

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
    from backend.mapping import map
    collection = getMongoCollection(api.name.lower())
    docs = map(items)
    # Add a system creation date
    for doc in docs:
        doc['_created']=now
    result = collection.insert_many(docs)
    return result

def delete(api: ApiEndpoint, id: str):
    collection = getMongoCollection(api.name.lower())
    result = collection.delete_one({"_id": id })

def getMongoResult(result: InsertManyResult) -> dict:
    ids = []
    for id in result.inserted_ids:
        ids.append(str(id))
    return { "acknowledged": str(result.acknowledged), "inserted_ids": ', '.join(ids) }