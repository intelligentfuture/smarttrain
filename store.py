from flask import Flask, render_template
from flask import request
from datetime import datetime
import sqlite3
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import json

app = Flask(__name__)

def database_init():
    db = sqlite3.connect('occupy.db')
    c = db.cursor()
    c.execute("create table if not exists occupy(ind integer primary key autoincrement,tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,node integer,previous real,occupy real);")
    db.commit()
    db.close()


@app.route("/update",methods=['POST'])
def update():
    args = dict(request.form)
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
        q = "INSERT INTO occupy(tstamp,node,previous,occupy) VALUES('%s',%s,%s,%s)"%(tstamp,node,previous,occupy)
        c.execute(q)
        db.commit()
        db.close()
        
        train_length=475.0
        
        p = float(previous)
        if(p>0.0):
            speed = train_length/p
            if(node=='60'):
                url = "http://blynk-cloud.com/caece42bd34043409ca9585dd393f068/update/A0?value=%f"%(speed)
                print(url)
                req = Request(url)
                
                with urlopen(req) as response:
                    reply = response.status
                    print(reply)

except Exception as e:
    print(e)
    resp['status'] = 'ERR'
    return json.dumps(resp)


def sendspeed(speed):
    chk = 0
    print(speed)
    url = 'http://blynk-cloud.com/caece42bd34043409ca9585dd393f068/update/A0?value=%s'%(speed)
    print(url)
    req = Request(url)
    with urlopen(req) as response:
        print(response.status())


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

