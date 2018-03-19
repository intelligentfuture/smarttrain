from flask import Flask, render_template
from flask import request
from datetime import datetime
import sqlite3
import json

app = Flask(__name__)

def database_init():
    db = sqlite3.connect('occupy.db')
    c = db.cursor()
    c.execute("create table if not exists occupy(ind integer primary key autoincrement,tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,node integer,previous real,occupy real);")
    db.commit()
    db.close()


@app.route("/update")
def update():
    args = dict(request.args)
    print(args)
    resp = dict()
    try:
        tstamp = args['tstamp'][0]
        node = args['node'][0]
        previous = args['previous'][0]
        occupy = args['occupy'][0]
        resp['status'] = 'OK'
    except:
        print("Wrong arguments")
        resp['status'] = 'ERR'
    try:
        db = sqlite3.connect('occupy.db')
        c = db.cursor()
        now = datetime.now()
        c.execute("INSERT INTO occupy(ind,tstamp,node,previous,occupy) VALUES(%d,'%s',%d,%d,%d)"%(ind,tstamp,node,previous,occupy))
        db.commit()
        db.close()
    except:
        print("Database error")
        resp['status'] = 'ERR'
    return json.dumps(resp)

@app.route("/check")
def check():
    resp = dict()
    try:
        resp['status'] = 'OK'
    except:
        print("Wrong arguments")
        resp['status'] = 'ERR'
    try:
        db = sqlite3.connect('occupy.db')
        c = db.cursor()
        c.execute("SELECT julianday(tstamp) from occupy ORDER BY tstamp DESC limit 1;")
        resp['result'] = c.fetchall()
        db.close()
    except:
        print("Database error")
        resp['status'] = 'ERR'
        db.close()

    return json.dumps(resp)

@app.route("/view")
def view():
    resp = dict()

    try:
        db = sqlite3.connect('occupy.db')
        c = db.cursor()
        c.execute("SELECT tstamp,node,previous,occupy from occupy ORDER BY tstamp DESC limit 10;")
        resp['result'] = c.fetchall()
        resp['status'] = 'OK'

        db.close()
    except:
        print("Database error")
        resp['status'] = 'ERR'
    try:
        if resp['status'] == 'OK':
            vlist = list()
            for v in resp['result']:
                vlist+=[v]
            return render_template('dis.html',items=vlist)
    except:
        print("Render error")

    return "error"



if __name__ == "__main__":
    database_init()
    app.run(host="0.0.0.0", port=5050)
    db.close()
