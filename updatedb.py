import sqlite3
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
    
resp = list()

def queryCheck():
    try:
        db = sqlite3.connect('occupy.db');
        c = db.cursor()
        c.execute("select julianday(tstamp) from occupy ORDER BY tstamp DESC limit 1;")
        resp = c.fetchall()
        db.close()
    except:
        #print("Database error")
        resp = []
    return resp

def queryUpdate(tstamp):
    try:
        db = sqlite3.connect('occupy.db');
        c = db.cursor()
        stm = "select tstamp,node,previous,occupy from occupy where julianday(tstamp) > %s;"%(tstamp)
        c.execute(stm)
        resp = c.fetchall()
        db.close()
    except:
        #print("Database error")
        resp = []
    return resp

def checkLast():
    chk = 0
    url = 'http://200ok.in.th:5050/check'
    request = Request(url)
    with urlopen(request) as response:
        repy = json.loads(response.read().decode('utf-8'))
        status = repy['status']
        result = repy['result'][0][0]
        if(status == 'OK'):
            chk = float(result)
    return chk

def update(res):
    chk = 0
    tstamp = res[0]
    node = res[1]
    previous = res[2]
    occupy = res[3]
    
    url = 'http://200ok.in.th:5050/update'
    data={'tstamp': tstamp, 'node': node, 'previous': previous, 'occupy': occupy}
    request = Request(url, urlencode(data).encode('utf-8'))

    with urlopen(request) as response:
        repy = json.loads(response.read().decode('utf-8'))
        status = repy['status']
        if(status == 'OK'):
            chk = 1
    return chk   

def checkForUpdate():
    chk = checkLast()
    if(chk > 0.0 and chk < queryCheck()[0][0]):
        #print("send update");
        val = queryUpdate(chk)
        for res in val:
            update(res)

#call for checking
checkForUpdate()