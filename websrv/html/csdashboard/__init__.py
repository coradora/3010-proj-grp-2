import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

# runs index() function when accessing host:5000 (127.0.0.1:5000 in webbrowser)
@app.route('/')
def index():
    conn = psycopg2.connect("host=192.168.56.20 dbname=student user=webuser1 password=ECUpirate1")
    cursor = conn.cursor()
    cursor.execute("SELECT \"ID\", concat(\"Honorific\", ' ',  \"First\", ' ',  \"Last\") AS \"Full Name\", \
        \"Email\", \"Phone\", \"Office\", \"ResearchInterests\" AS \"Research Interests\", \
        \"Rank\", \"Remarks\", \"CurrentlyEmployed\" AS \"Currently Employed\"\
        FROM csdashboard ORDER BY \"ID\"")
    record = cursor.fetchall()
    if record == -1:
        print('SQL command error')
    else:
        col_names = [desc[0] for desc in cursor.description]
        log = record[:20]
    return render_template('index.html', sql_table = log, table_title=col_names)

@app.route('/history')
def history():
    conn = psycopg2.connect("host=192.168.56.20 dbname=student user=webuser1 password=ECUpirate1")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM csdashboard") # change to appropriate SQL query
    record = cursor.fetchall()
    if record == -1:
        print('SQL command error')
    else:
        col_names = [desc[0] for desc in cursor.description]
        log = record[:20]
    return render_template('index.html', sql_table = log, table_title=col_names)

if __name__ == "__main__":
    app.run('127.0.0.1')