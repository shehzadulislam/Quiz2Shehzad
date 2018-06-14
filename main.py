# Shehzad ul Islam - 1001555356

import os
import csv
import sqlite3
import pandas as pd
import datetime
import time
# import random
from sqlite3 import Error
import memcache


from flask import Flask, render_template, request
app = Flask(__name__)

__author__ = 'Shehzad'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def readcsvinsertdata(conn,filename):
    with open(filename, 'r') as csvfile:
        df = pd.read_csv(csvfile)

        df.columns = df.columns.str.strip()
        # cur = conn.cursor()

        # cur.execute('SELECT * FROM People')
        # rows = cur.fetchall()
        # if len(rows) == 0:
        df.to_sql('Earthquakes', conn, if_exists='append', index=False)
        # readCSV = csv.reader(csvfile, delimiter=',')
        # next(readCSV)
        # cur = conn.cursor()
        # cur.execute('SELECT * FROM classes')
        # rows = cur.fetchall()
        # if len(rows) == 0:
        #     for row in readCSV:
        #         conn.execute("INSERT INTO classes ( ID,Days, Start, End, Approval ,Max ,Current ,Seats ,Wait ,Instructor ,Course,Section ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]))
        #     conn.commit()

# def main():
#     database = "Quiz2.db"
#     conn = create_connection(database)
    # sql_create_courses_table = """ CREATE TABLE IF NOT EXISTS classes (
    #                                     ID integer,
    #                                     Days text,
    #                                     Start text,
    #                                     End text,
    #                                     Approval text,
    #                                     Max text,
    #                                     Current text,
    #                                     Seats text,
    #                                     Wait text,
    #                                     Instructor text,
    #                                     Course text,
    #                                     Section text
    #                                 ); """


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/uploadCSVfile')
def uploadcsvfile():
    return render_template('uploadcsv.html')

@app.route('/uploadimagefile')
def uploadimagefile():
    return render_template('uploadimage.html')

@app.route('/uploadcsv', methods=['POST'])
def uploadCSV():
    target = os.path.join(APP_ROOT)
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    # create a database connection
    conn = create_connection("Assignment3.db")
    if conn is not None:
            # create table
            # create_table(conn, sql_create_courses_table)
        readcsvinsertdata(conn,file.filename)
    else:
        print("Error! cannot create the database connection.")

    return render_template("complete.html")

@app.route('/uploadimage', methods=['POST'])
def uploadImage():
    target = os.path.join(APP_ROOT, 'static/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    return render_template("complete.html")

@app.route('/list' ,methods = ['POST', 'GET'])
def coursesname():
    con = sqlite3.connect("Assignment3.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM Earthquakes')
    rows = cur.fetchall()
    print(len(rows))
    print(rows)
    return render_template("list.html", rows=rows)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/magnitude', methods=['POST'])
def grmag():
    loc = request.form['location']
    print(loc)
    mag = request.form['magnitude']
    print(mag)
    conn = sqlite3.connect("Assignment3.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # cursor.execute('Select time,latitude,longitude,place from Earthquakes where mag > ? AND locationSource = ?', (mag,loc,))
    cursor.execute('Select time,latitude,longitude,place from Earthquakes where mag > ? AND locationSource = ? AND CAST(magNst AS INTEGER) * 2 >= CAST(nst AS INTEGER)', (mag,loc,))
    rows = cursor.fetchall()
    # cursor.execute('Select gap from Earthquakes where gap < ?', (gapfrom,))
    # below = cursor.fetchall()
    # cursor.execute('Select gap from Earthquakes where gap > ?', (gapto,))
    # above = cursor.fetchall()
    return render_template('result.html', row = rows, number = len(rows))

@app.route('/randomquery')
def randomquery():
    return render_template('performancemeasure.html')

@app.route('/randommemquery')
def randommemquery():
    return render_template('performancemeasuremem.html')


@app.route('/random', methods=['POST'])
def randomqueries():
    numberofqueries = request.form['number']
    conn = sqlite3.connect("Assignment3.db")
    # coll =[]
    # starttime = time.time()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('Delete from Earthquakes where rms <= ?', (numberofqueries,))
    # for loop in range(1, int(numberofqueries) + 1):
    #     randnum = random.randrange(0,10)
    #     magnitude = int(randnum)
    #     cursor.execute('Select time from Earthquakes where mag >= ?', (magnitude,))
    #     data = cursor.fetchall()
    # endtime = time.time()
    # diff = endtime - starttime
    # loop = 0
    return render_template('performancemeasure.html')

# @app.route('/randommem', methods=['POST'])
# def randommemqueries():
#     conn = sqlite3.connect("Assignment3.db")
#     cursor = conn.cursor()
#     mc = memcache.Client(['127.0.0.1:11211'], debug=1)
#     numberofqueries = request.form['number']
#     start_time = time.time()
#     for loop in range(1, int(numberofqueries) + 1):
#         randnum = random.randrange(0,10)
#         query = 'Select time from Earthquakes where mag >= ?', (randnum,)
#         key = str(query)
#         value = mc.get(key)
#         if value is None:
#             statement = sqlite3.prepare(conn, query)
#             cursor.execute(statement)
#             rows = []
#             #obtaining the results
#             data = cursor.fetchone()
#             while res != False:
#                  rows.append(data)
#                  res = cursor.fetchone()
#             result = " "
#             for i in rows:
#                result += str(i)
#             status = mc.set(key, result)
#         else:
#                 inside = inside + 1
#                 mc.get(key)
#     end_time = time.time()
#     diff = end_time - start_time
#     return render_template('performancemeasuremem.html', totaltime = diff)
    # conn = sqlite3.connect("Assignment3.db")
    # cursor = conn.cursor()
    # mc = memcache.Client(['127.0.0.1:11211'], debug=1)
    # numberofqueries = request.form['number']
    # val = numberofqueries
    # start_time = time.time()
    # inside = 0
    # for loop in range(1, int(numberofqueries) + 1):
    #     query = "select mag from Earthquakes"
    #     key = query.replace(' ', '')
    #     value = mc.get(key)
    #     if value is None:
    #         statement = query
    #         cursor.execute(statement)
    #         rows = []
    #         # obtaining the results
    #         res = cursor.fetchall()
    #         result = " "
    #         for i in res:
    #             result += str(i)
    #         status = mc.set(key, result)
    #     else:
    #         inside = inside + 1
    #         mc.get(key)

PORT = int(os.getenv('PORT','5000'))
if __name__ == '__main__':
    # main()
    app.run(debug=True)

# import os
# import random
# import memcache
# from flask import Flask, redirect, render_template, request
# from time import time
# import json
# import ibm_db
#
# # _name_ is set to the name of the current class, function, method, descriptor, or generator instance.
# app = Flask(_name_)
# memc = memcache.Client(['127.0.0.1:11211'], debug = 1)
#
# dataset=['ak','ci','hv','ismp','ld','mb','nc','nm','nn','ott','pr','se','tul','us','uu','uw']
#
# # get service information if on IBM Cloud Platform
# if 'VCAP_SERVICES' in os.environ:
#     db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
#     db2cred = db2info["credentials"]
#     appenv = json.loads(os.environ['VCAP_APPLICATION'])
# else:
#     # raise ValueError('Expected cloud environment')
#     with open('connections.json') as new_file_db:
#         new_file = json.load(new_file_db)
#         db2info = new_file['dashDB For Transactions'][0]
#         db2cred = db2info["credentials"]
#
# @app.route('/searchtwo', methods=['POST'])
# def searchtwo():
#
#     conn = ibm_db.connect(
#         "DATABASE=" + db2cred['db'] + ";HOSTNAME=" + db2cred['hostname'] + ";PORT=" + str(db2cred['port']) + ";UID=" +
#         db2cred['username'] + ";PWD=" + db2cred['password'] + ";", "", "")
#     if conn:
#         # we have a Db2 connection, query the database
#         selection = request.form['selection']
#         if(selection=='location'):
#             locsrc = request.form['loc']
#
# r = random.uniform(0.5, 6.0)
# sequel = "select mag from equake where locationSource = ? "#and mag = ?"
# # Note that for security reasons we are preparing the statement first,
# statement = ibm_db.prepare(conn, sequel)
# ibm_db.bind_param(statement, 1, location)
# # ibm_db.bind_param(statement, 2, r)
# ibm_db.execute(statement)

# def memmagnitude(range1, range2,iteration):
#     conn = ibm_db.connect(
#         "DATABASE=" + db2cred['db'] + ";HOSTNAME=" + db2cred['hostname'] + ";PORT=" + str(db2cred['port']) + ";UID=" +
#         db2cred['username'] + ";PWD=" + db2cred['password'] + ";", "", "")
#     val = iteration
#
#     start_time = time()
#     inside = 0
#     count = 1
#     while (count <= val):
#         loc_query = "select mag from equake where mag between " + range1 + " and "+range2
#         new_key = loc_query.replace(' ', '')
#         value = memc.get(new_key)
#         if value is None:
#             print("first time put")
#             statement = ibm_db.prepare(conn, loc_query)
#             ibm_db.execute(statement)
#             rows = []
#             # obtaining the results
#             res = ibm_db.fetch_assoc(statement)
#             while res != False:
#                 rows.append(res.copy())
#                 res = ibm_db.fetch_assoc(statement)
#
#             result = " "
#             for i in rows:
#                 result += str(i)
#
#             status = memc.set(new_key, result)
#
#         else:
#             inside = inside + 1
#
#             memc.get(new_key)
#
#         count = count + 1
#     print(inside)
#     end_time = time()
#     print('end_time')
#     total_sqltime = end_time - start_time
#     print(total_sqltime)
#     return render_template('view3.html', rows=total_sqltime)

# @app.route('/addrec',methods = ['POST', 'GET'])
# def addrec():
#    if request.method == 'POST':
#       try:
#          nm = request.form['nm']
#          addr = request.form['add']
#          city = request.form['city']
#          pin = request.form['pin']

#          with sql.connect("database.db") as con:
#             cur = con.cursor()

#             cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )

#             con.commit()
#             msg = "Record successfully added"
#       except:
#          con.rollback()
#          msg = "error in insert operation"

#       finally:
#          return render_template("result.html",msg = msg)
#          con.close()

# @app.route('/list')
# def list():
#    con = sql.connect("database.db")
#    con.row_factory = sql.Row

#    cur = con.cursor()
#    cur.execute("select * from students")

#    rows = cur.fetchall();
#    return render_template("list.html",rows = rows)