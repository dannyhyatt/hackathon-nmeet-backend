from flask import Flask, request, jsonify
import psycopg2 as psycopg2
import creds as creds
import os

conn_string = "host="+ creds.PGHOST +" port="+ "5432" +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER \
+" password="+ creds.PGPASSWORD
print('conn string: ' + conn_string)
conn=psycopg2.connect(conn_string)
print("connected to db!")

cur = conn.cursor()

# export FLASK_ENV=development
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/home/danny/Documents/nomeet-server/pics/'
@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/signup", methods=['POST'])
def signup():
    print('yuh')
    try:
        cur.execute("INSERT INTO users (name, username, password, latitude, longitude) VALUES (%s, %s, %s, %s, %s);", (request.form['name'], request.form['username'], request.form['password'], request.form['lat'], request.form['lng']))
        #cur.execute("INSERT INTO \"users\" (name, username, password) VALUES ('danny','danny','danny');")
        conn.commit()
        print('suckesksks')
        return jsonify({"success" : True})
    except Exception as e:
        print("error 1 is " + str(e))
        if str(e.__class__) == "<class 'psycopg2.errors.UniqueViolation'>":
            cur.execute("ROLLBACK") # needs to happen when postgres runs into an error, maybe alternative is create new cursor
            conn.commit()
            print("yuh2")
        return jsonify({"success" : False, "error" : "unknown"})


@app.route("/login", methods=['POST'])
def login():
    print('login')
    try:
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s;", (request.form['username'], request.form['password']))
        results = cur.fetchall()
        valid = False
        for _ in results:
            #print("Id = ", row[0], )
            valid = True # on first match set to true, only needs to be one
        if valid:
            return jsonify({"success" : True})
        else: 
            return jsonify({"success" : False, "error" : "incorrect password"})
    except Exception as e:
        print("error 2 is " + str(e))
        return jsonify({"success" : False, "error" : "unknown"})

@app.route('/uploadSelfie', methods = ['POST'])
def uploadSelfie():
    f = request.files['file']
    f.save(app.config['UPLOAD_FOLDER'] + 'known/' + request.form['username'] + '.jpg')
    return jsonify({"success" : True})