import xlrd
from flask import Flask
from flask import render_template
from flask import request
import json
import pymongo
from pymongo import Connection
from pymongo.errors import AutoReconnect
try:
    # mongoConn = Connection(host=MGDBS['HOST'],port=MGDBS['PORT'])
    host_url = '%s:%i,%s:%i'%('localhost',27017,'localhost',27018)
    mongoConn = pymongo.MongoReplicaSetClient(host=host_url, replicaSet='zhs_replset', read_preference=pymongo.ReadPreference.PRIMARY_PREFERRED)

except AutoReconnect,e:
    print "init mongo connection failed.... "
    mongoConn = None

app = Flask(__name__)

db = mongoConn['search']['items']
value_list = []
def read_excel(file_name):
    data  = xlrd.open_workbook(file_name)
    table = data.sheets()[0]
    nrows = table.nrows
    for i in range(0, nrows):
        value_list.append(table.row_values(i))

def read_from_mongo():
    cursor = db.find({},{'values':1,'id':1})
    for item in cursor:
        del item['_id']
        value_list.append(item)

def search_school(school):
    res = []
    for item in value_list:
        if item['values'][3].find(school) >= 0:
            tmp = {'id':item['id'],'data':[]}
            tmp_list = item['values'][3].split(school)
            for i in range(0, len(tmp_list) -1):
                tmp['data'].append(tmp_list[i][-7:] + school + tmp_list[i + 1][:7])
            res.append(tmp)
    return res

@app.route('/')
def index():
    return render_template('index.html')    

@app.route('/search')
def search():
    school = request.args.get('school')
    res = search_school(school)
    return json.dumps({"success":True,"data":res})

@app.route('/mark')
def mark():
    school = request.args.get('school')
    id = request.args.get('id')
    db.update({'id':int(id)},{"$set":{school:1}})
    return '',200

if __name__ == '__main__':
    #read_excel('boardmember1.xlsx')
    read_from_mongo()    
    app.run(debug=True, host='0.0.0.0')
