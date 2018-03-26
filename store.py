from flask import Flask, render_template
from flask import request
from datetime import datetime
import sqlite3
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

train_length=475.0
rail_length=3400.0

def database_init():
    db = sqlite3.connect('occupy.db')
    c = db.cursor()
    c.execute("create table if not exists occupy(ind integer primary key autoincrement,tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,node integer,previous real,occupy real,speed real);")
    db.commit()
    db.close()


def dict_factory(cursor, row):
    d = []
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/update",methods=['POST'])
def update():
    args = dict(request.form)['update'][0]

    js = json.loads(args)
    resp = dict()
    resp['status'] = 'ERROR'

    for args in js:
        try:
            tstamp = args['tstamp']
            node = args['node']
            previous = args['previous']
            occupy = args['occupy']
            resp['status'] = 'OK'
        except:
            print("Wrong arguments")
            resp['status'] = 'ERR'
        try:
            
            p = float(previous)
            o = float(occupy)
            speed=0.0
            
            if(p==0.0):
                speed = train_length/o
            else:
                speed = (rail_length-train_length)/p

            if(speed!=0):
                sendspeed(node,speed)
            
        
            db = sqlite3.connect('occupy.db')
            c = db.cursor()
            q = "INSERT INTO occupy(tstamp,node,previous,occupy,speed) VALUES('%s',%s,%s,%s,%s)"%(tstamp,node,previous,occupy,str(speed))
            c.execute(q)
            db.commit()
            db.close()

        except Exception as e:
            print(e)
            resp['status'] = 'ERR'

    return json.dumps(resp)


def sendspeed(node,speed):
    url = "http://blynk-cloud.com/caece42bd34043409ca9585dd393f068/update/A0?value=%f"%(speed)
    req = Request(url)
    with urlopen(req) as response:
        reply = response.status


@app.route("/check")
def check():
    args = dict(request.args)
    resp = dict()
    try:
        node = args['node'][0]
        resp['status'] = 'OK'
    except:
        print("Wrong arguments")
        resp['status'] = 'ERR'
    try:
        db = sqlite3.connect('occupy.db')
        c = db.cursor()
        c.execute("SELECT julianday(tstamp) from occupy where node=%s ORDER BY tstamp DESC limit 1;"%(node))
        resp['result'] = c.fetchall()
        if(len(resp['result'])==0):
            resp['result']=[[1]]
        db.close()
    except:
        print("Database error")
        resp['status'] = 'ERR'
        db.close()

    return json.dumps(resp)



@app.route("/api/active")
def getactive():
    args = dict(request.args)
    resp = dict()
    resp['status'] = 'ERR'
    try:
        node = args['node'][0]
        resp['status'] = 'OK'
    except:
        print("Wrong arguments")
        resp['status'] = 'ERR'
    try:
        db = sqlite3.connect('occupy.db')
        c = db.cursor()
        c.execute("SELECT node,speed from occupy group by node ORDER BY tstamp DESC limit 4;")
        recs = c.fetchall()
        data = list()
        clist = [tuple[0] for tuple in c.description]
        for v in recs:
            d = {}
            for i in range(0,len(clist)):
                d.update({clist[i]:v[i]})
            data.append(d)
        return jsonify(data)
    except Exception as e:
        print(e)
        db.close()
    
    return json.dumps(resp)



@app.route("/api/speed")
def speed():
    args = dict(request.args)
    resp = dict()
    resp['status'] = 'ERR'
    try:
#        node = args['node'][0]
        resp['status'] = 'OK'
    except:
        print("Wrong arguments")
        resp['status'] = 'ERR'
    try:
        db = sqlite3.connect('occupy.db')
        c = db.cursor()
        c.execute("SELECT node,previous,occupy,speed from occupy group by node ORDER BY tstamp DESC limit 4;")
        recs = c.fetchall()
        data = list()
        clist = [tuple[0] for tuple in c.description]
        for v in recs:
            d = {}
            for i in range(0,len(clist)):
                d.update({clist[i]:v[i]})
            data.append(d)
        return jsonify(data)
    except Exception as e:
        print(e)
        db.close()
    
    return json.dumps(resp)


@app.route("/api/timetable")
def timetable():
    args = dict(request.args)
    resp = dict()
    resp['status'] = 'ERR'
    try:
        resp['status'] = 'OK'
    except:
        print("Wrong arguments")
        resp['status'] = 'ERR'
    try:
        db = sqlite3.connect('occupy.db')
        c = db.cursor()
        c.execute("SELECT distinct tstamp,node,previous,occupy,speed from occupy where previous<>0 ORDER BY tstamp DESC limit 10;")
        recs = c.fetchall()
        data = list()
        clist = [tuple[0] for tuple in c.description]
        for v in recs:
            d = {}
            for i in range(0,len(clist)):
                d.update({clist[i]:v[i]})
            data.append(d)
        return jsonify(data)
    except Exception as e:
        print(e)
        db.close()
    return json.dumps(resp)


@app.route("/view")
def view():
    resp = dict()

    try:
        db = sqlite3.connect('occupy.db')
        c = db.cursor()
        c.execute("SELECT distinct tstamp,node,previous,occupy,speed from occupy where previous<>0 ORDER BY tstamp DESC limit 10;")
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
