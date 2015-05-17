import xlrd
from flask import Flask
from flask import render_template
from flask import request
import json
app = Flask(__name__)


value_list = []
def read_excel(file_name):
    data  = xlrd.open_workbook(file_name)
    table = data.sheets()[0]
    nrows = table.nrows
    for i in range(0, nrows):
        value_list.append(table.row_values(i))

def search_school(school):
    res = '<table>'
    row = 0
    for item in value_list:
        if item[3].find(school) >= 0:
            temp = item[3].replace(school, '<font color="red">%s</font>' % school)
            res += '<tr><td><input type="checkbox" id="%d"></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (row, item[0], item[1], item[2], temp)
        row += 1
    return res

@app.route('/')
def index():
    return render_template('index.html')    

@app.route('/search')
def search():
    school = request.args.get('school')
    res = search_school(school)
    return json.dumps({"success":True,"data":res})

if __name__ == '__main__':
    read_excel('boardmember1.xlsx')    
    app.run(debug=True)
