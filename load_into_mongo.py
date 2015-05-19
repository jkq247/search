import xlrd
import pymongo

conn = pymongo.MongoClient('localhost', 27017)
db = conn['search']['items']

def read_excel(file_name):
    data  = xlrd.open_workbook(file_name)
    table = data.sheets()[0]
    nrows = table.nrows
    for i in range(235248, nrows):
        print i
        db.update({'id':i},{'$set':{'values':table.row_values(i)}},upsert=True)

if __name__ == '__main__':
    read_excel('boardmember.xlsx')
