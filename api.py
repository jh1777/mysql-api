from flask import Flask, request, jsonify
import pymysql
import pymysql.cursors
from jsonEncoder import MyJSONEncoder
from gehaltApi import gehalt_api
# pip3 install simplejson
# pip3 install pymysql
# pip3 install flask

import json
app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

app.config["DEBUG"] = True
app.json_encoder = MyJSONEncoder
app.register_blueprint(gehalt_api, url_prefix='/salary/v1')

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''



@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/gehalt/<jahr>', methods=['GET'])
def api_gehalt(jahr):
    # Connect to the database
    db = pymysql.connect(host=app.config["DB_IP"],
                                user=app.config["DB_USERNAME"],
                                password=app.config["DB_PASSWORD"],
                                database=app.config["DB_NAME"],
                                cursorclass=pymysql.cursors.DictCursor)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("select * from Gehalt where Jahr = " + jahr)

    # Fetch a single row using fetchone() method.
    #data = cursor.fetchone()
    #print ("Database version : %s " % data)

    data = cursor.fetchall()

    # disconnect from server
    db.close()
    return jsonify(data)

@app.route('/api/v1/resources/books/<int:id>', methods=['GET'])
def api_id(id):
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    
    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == "__main__":
    app.run()