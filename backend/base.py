
import pymysql
import pymysql.cursors
import connexion

app = connexion.App(__name__)
app.app.config.from_object("config.DevelopmentConfig")

def connectToDb():
    # Connect to the database
    db = pymysql.connect(host=app.app.config["DB_IP"],
                                user=app.app.config["DB_USERNAME"],
                                password=app.app.config["DB_PASSWORD"],
                                database=app.app.config["DB_NAME"],
                                cursorclass=pymysql.cursors.DictCursor)
    return db

def queryDb(queryString: str):
    # Connect
    db = connectToDb()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute(queryString)
    data = cursor.fetchall()

    # disconnect from server
    db.close()

    return data
