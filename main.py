# Shehzad ul Islam - 1001555356

import os
import csv
import sqlite3
import pandas as pd
import datetime
import time
import random
from sqlite3 import Error
# from ibmdbpy import IdaDataBase, IdaDataFrame


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

@app.route('/random', methods=['POST'])
def randomqueries():
    numberofqueries = request.form['number']
    conn = sqlite3.connect("Assignment3.db")
    cursor = conn.cursor()
    starttime = time.time()
    for loop in range(1, int(numberofqueries) + 1):
        randnum = random.randrange(0,100)
        print(randnum)
        cursor.execute('Select time from Earthquakes where mag >= ?', (randnum,))
        data = cursor.fetchall()
        print(randnum)
    endtime = time.time()
    diff = endtime - starttime
    print(diff)
    return render_template('performancemeasure.html', time = diff)

PORT = int(os.getenv('PORT','5000'))
if __name__ == '__main__':
    # main()
    app.run(debug=True)


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