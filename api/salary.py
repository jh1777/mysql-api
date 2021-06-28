import pymysql
import pymysql.cursors
import connexion

app = connexion.FlaskApp(__name__)
app.app.config.from_object("config.DevelopmentConfig")

def create():
    return  "Created"

def getAll():
    return "Get All entries"

def getById(id):
    # Connect to the database
    db = pymysql.connect(host=app.app.config["DB_IP"],
                                user=app.app.config["DB_USERNAME"],
                                password=app.app.config["DB_PASSWORD"],
                                database=app.app.config["DB_NAME"],
                                cursorclass=pymysql.cursors.DictCursor)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("select * from Gehalt where Id = " + format(id))
    data = cursor.fetchall()

    # disconnect from server
    db.close()

    if (not data):
        return None, 404

    return data, 200
    
def getByYear(year):
    # Connect to the database
    db = pymysql.connect(host=app.app.config["DB_IP"],
                                user=app.app.config["DB_USERNAME"],
                                password=app.app.config["DB_PASSWORD"],
                                database=app.app.config["DB_NAME"],
                                cursorclass=pymysql.cursors.DictCursor)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("select * from Gehalt where Jahr = " + format(year))

    data = cursor.fetchall()

    # disconnect from server
    db.close()

    if (not data):
        return None, 404
    
    return data, 200