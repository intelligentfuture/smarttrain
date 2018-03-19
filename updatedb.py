import sqlite3
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import time

resp = list()
node_list = list()

def getNode():
    try:
        db = sqlite3.connect('occupy.db')
        c = db.cursor()
        c.execute("select distinct node from occupy;")
        node_list = c.fetchall()
        db.close()
    except Exception as e:
        print(e)
    return node_list


def queryCheck(node):
    try:
        db = sqlite3.connect('occupy.db');
        c = db.cursor()
        c.execute("select julianday(tstamp) from occupy where node=%s order BY tstamp desc limit 1;"%(node))
        resp = c.fetchall()
        db.close()
    except Exception as e:
        print(e)
        resp = []
    return resp

def queryUpdate(tstamp, node):
    try:
        db = sqlite3.connect('occupy.db');
        c = db.cursor()
        stm = "select tstamp,node,previous,occupy from occupy where (node=%s and julianday(tstamp) > %s);"%(node, tstamp)
        #print(stm)

        c.execute(stm)
        resp = c.fetchall()
        db.close()
    except Exception as e:
        print(e)
        resp = []
    return resp

def checkLast(node):
    chk = 0
    url = 'http://200ok.in.th:5050/check?node=%s'%(node)
    request = Request(url)
    try:
        with urlopen(request) as response:
            repy = json.loads(response.read().decode('utf-8'))
            status = repy['status']
            result = repy['result'][0][0]
            if(status == 'OK'):
                chk = float(result)
    except Exception as e:
        print(e)
    return chk

def update(data):
    chk = 0
    url = 'http://200ok.in.th:5050/update'
    request = Request(url, urlencode(data).encode('utf-8'))
    try:
        with urlopen(request) as response:
            repy = json.loads(response.read().decode('utf-8'))
            status = repy['status']
            if(status == 'OK'):
                chk = 1
    except Exception as e:
        print(e)
    return chk

def checkForUpdate(node):
    chk = checkLast(node)
    if(chk > 0 and chk < queryCheck(node)[0][0]):
        #print("send update");
        val = queryUpdate(chk, node)
        sendObj = {}
        tmplist = []
        tmp = dict()
        for res in val:
            tmp['tstamp'] = res[0]
            tmp['node'] = res[1]
            tmp['previous'] = res[2]
            tmp['occupy'] = res[3]
            tmplist += [tmp]
#        sendObj[str(node)] = tmplist
        sendObj['update'] = json.dumps(tmplist)
        update(sendObj)

def updateDB():
    for _node in getNode():
        checkForUpdate(_node[0])
    time.sleep(10) # wait 10 sec for next update

while(1):
    updateDB()
