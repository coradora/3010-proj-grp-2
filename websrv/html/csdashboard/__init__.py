import psycopg2
from flask import Flask, render_template, request, url_for,redirect
app = Flask(__name__)

class DataTable:
    def __init__(self, query):
        self.conn = psycopg2.connect("host=192.168.56.20 dbname=student user=webuser1 password=ECUpirate1")
        self.cursor = self.conn.cursor()

        self.query = self.cursor.execute(query)
        self.record = self.cursor.fetchall()

        if self.record == -1:
            print("SQL query error")
        else:
            self.col_names = [desc[0] for desc in self.cursor.description]
            #self.log = self.record[:20]
            self.log = self.record


@app.route('/')
def root():
    table = DataTable("SELECT id, concat(honorific, ' ', first, ' ', last) AS \"Full Name\", \
                        email, phone, office, researchinterests AS \"Research Interests\", \
                          rank, remarks, currentlyemployed AS \"Currently Employed\"\
                          FROM csdashboard ORDER BY id")
    return render_template('index.html', sql_table = table.log, table_title=table.col_names)

# runs index() function when accessing localhost/hostname (127.0.0.1 in webbrowser)
@app.route('/<table_name>')
@app.route('/<table_name>/page/<int:page>')
def index(table_name, page=1):
    print(table_name)
    offset = (page - 1) * 10
    if(table_name == 'faculty'):
        table = DataTable(f"SELECT concat(honorific, ' ', first, ' ', last) AS \"Full Name\", \
                        email AS \"E-Mail\", phone AS \"Phone\", office AS \"Office\", researchinterests AS \"Research Interests\", \
                          rank AS \"Rank\", remarks AS \"Remarks\", currentlyemployed AS \"Currently Employed\"\
                          FROM csdashboard ORDER BY id LIMIT 10 OFFSET {offset}")
    
    elif(table_name == 'history'):
        table = DataTable("SELECT CONCAT(classhistory.prefix, ' ', classhistory.number) as \"Course\", courses.title AS \"Title\", \
                                CONCAT(csdashboard.honorific, ' ', csdashboard.first, ' ', csdashboard.last) as \"Instructor\", \
                                year AS \"Year\", semester AS \"Semester\", section AS \"Section\", crn AS \"CRN\", \
                                enrollment AS \"Enrollment\", days AS \"Days\", begin_time AS \"Begin Time\", end_time AS \"End Time\" \
                            FROM classhistory \
                            JOIN courses ON classhistory.prefix = courses.prefix AND classhistory.number = courses.number \
                            JOIN csdashboard ON classhistory.instructor = csdashboard.id")  

    # TODO: Clean up table, join with Courses table to display course title & 
    #        csdashboard table to display instructor instead of instructor ID 
    elif(table_name == 'faculty_committees'):
        table = DataTable("SELECT * FROM faculty_committees")  
    
    elif(table_name == 'courses'):
       table = DataTable("SELECT concat(prefix, ' ', number) AS \"Number\", title as \"Title\", gu AS \"GU\", ch AS \"CH\", \
                         frequency AS \"Frequency\", active AS \"Active\", description AS \"Description\" FROM courses\
                            ORDER BY id") 

    elif(table_name == 'fte'):
       table =DataTable("SELECT CONCAT(honorific, ' ', first, ' ', last) AS \"Faculty\", \
                        year AS \"Year\", semester AS \"Semester\", \
                            TRUNC(SUM(CASE \
                                WHEN courses.prefix = 'CSCI' AND courses.gu = 'U' \
                                    THEN (courses.ch * classhistory.enrollment)/406.24 \
                                WHEN courses.prefix = 'CSCI' AND courses.gu = 'G' \
                                    THEN (courses.ch * classhistory.enrollment)/186.23 \
                                WHEN courses.prefix = 'SENG' AND courses.gu = 'U' \
                                    THEN (courses.ch * classhistory.enrollment)/232.25 \
                                WHEN courses.prefix = 'SENG' AND courses.gu = 'G' \
                                    THEN (courses.ch * classhistory.enrollment)/90.17 \
                                WHEN courses.prefix = 'DASC' AND courses.gu = 'G' \
                                    THEN (courses.ch * classhistory.enrollment)/186.23 ELSE 0 \
                            END), 2) AS \"FTE\" \
                        FROM csdashboard \
                        JOIN classhistory on csdashboard.id = classhistory.instructor \
                        JOIN courses ON courses.number = classhistory.number \
                        GROUP BY csdashboard.id, classhistory.year, classhistory.semester \
                        ORDER BY year DESC, csdashboard.last ASC")

    if request.method == "POST":
        search_term = request.form.get(table.col_names)
        print(search_term)

    return render_template('index.html', sql_table = table.log, table_title=table.col_names, table_name = table_name, current_page=page)



@app.route('/admin')
def admin():
    query = request.args.get('query')
    print(query)
    result = []
    # TODO: use regex to check query string for bad words 'DROP'/'CREATE' etc. Can make this page an admin dashboard?
    if query:
        search = DataTable(query)
        # result = DataTable.cursor.execute(f"SELECT * FROM  csdashboard where column like '%{query}%").fetchall()
    search = DataTable("SELECT * FROM csdashboard")
    return render_template('search.html',sql_table = search.log, table_title=search.col_names,result=result)



if __name__ == "__main__":
    app.run('127.0.0.1')