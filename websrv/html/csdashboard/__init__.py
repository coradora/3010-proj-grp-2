import psycopg2
import re
from flask import Flask, render_template, request
app = Flask(__name__)

# Custom class for DataTable. Each DataTable initializes a connection to the database, creates a cursor,
# and executes a query provided in the index function below. Fetches all results and records it in the table.
class DataTable:
    def __init__(self, query):
        self.conn = psycopg2.connect("host=192.168.56.20 dbname=student user=webuser1 password=ECUpirate1")
        self.cursor = self.conn.cursor()

        try:
            # Executes query on postgresql
            self.query = self.cursor.execute(query)
            # Fetches query data, stores in record.
            self.record = self.cursor.fetchall()

            if self.record == -1:
                print("SQL query error")
                
            else:
                # Sort column contents in descending order.
                self.col_names = [desc[0] for desc in self.cursor.description]
                self.log = self.record
        # If SQL query throws an exception, set log value to 0.
        except Exception as err:
            self.log = 0

# Same as faculty condition in index function. Covers the case of accessing 127.0.0.1 w/ no specified tables.
@app.route('/')
def root():
    table = DataTable(f"SELECT concat(honorific, ' ', first, ' ', last) AS \"Name\", rank AS \"Rank\", \
                        email AS \"E-Mail\", phone AS \"Phone\", office AS \"Office\", researchinterests AS \"Research Interests\", \
                        remarks AS \"Remarks\", last FROM csdashboard ORDER BY id")
    return render_template('index.html', sql_table = table.log, table_title=table.col_names)

# runs index() function when accessing localhost/hostname (127.0.0.1 in webbrowser)
# Searching/sorting is accomplished on the front-end through JQuery, input sanitization is only necessary
# for the address bar. We ensure that the data the user may manually input is a string value. 
@app.route('/<string:table_name>')
# @app.route('/<table_name>/page/<int:page>')
def index(table_name, page=1):
    print(table_name)

    # If user provides their own link, return an error if > 20 characters. 
    # (User should only be navigating pages through navbar)
    if(len(table_name) > 20):
        return render_template('error.html')
    # Messy SQL queries
    # TODO: Refactor? Store queries in another file?

    # Generates table based on the following SQL queries where table_name == url name.
    # 127.0.0.1/faculty table. Displays faculty and their information.
    if(table_name == 'faculty'):
        table = DataTable(f"SELECT concat(honorific, ' ', first, ' ', last) AS \"Name\", rank AS \"Rank\", \
                        email AS \"E-Mail\", phone AS \"Phone\", office AS \"Office\", researchinterests AS \"Research Interests\", \
                        remarks AS \"Remarks\" FROM csdashboard ORDER BY id")
    
    # 127.0.0.1/historytable. Displays course history, their enrollment, sections, and dates.
    elif(table_name == 'history'):
        table = DataTable("SELECT CONCAT(classhistory.prefix, ' ', classhistory.number) as \"Course\", courses.title AS \"Title\", \
                                CONCAT(csdashboard.honorific, ' ', csdashboard.first, ' ', csdashboard.last) as \"Instructor\", \
                                year AS \"Year\", semester AS \"Semester\", section AS \"Section\", crn AS \"CRN\", \
                                enrollment AS \"Enrollment\", days AS \"Days\", begin_time AS \"Begin Time\", end_time AS \"End Time\" \
                            FROM classhistory \
                            JOIN courses ON classhistory.prefix = courses.prefix AND classhistory.number = courses.number \
                            JOIN csdashboard ON classhistory.instructor = csdashboard.id")  

    # 127.0.0.1/faculty_committees table. Displays faculty committees and the faculty member that leads them.
    elif(table_name == 'faculty_committees'):
        table = DataTable("select CONCAT(honorific, ' ', first, ' ', last) AS Instructor, committee_name \
                            AS \"Committee Name\", start_date AS Start, end_date AS End from faculty_committees \
                            JOIN csdashboard ON faculty_committees.faculty_id = csdashboard.id \
                            JOIN committee_names ON faculty_committees.committee_id = committee_names.id \
                            WHERE faculty_committees.faculty_id = csdashboard.id AND faculty_committees.committee_id = committee_names.id;")  

    # 127.0.0.1/courses table. Displays course in catalog and their information.          
    elif(table_name == 'courses'):
       table = DataTable("SELECT concat(prefix, ' ', number) AS \"Number\", title as \"Title\", gu AS \"GU\", ch AS \"CH\", \
                         frequency AS \"Frequency\", active AS \"Active\", description AS \"Description\" FROM courses\
                            ORDER BY id") 

    # 127.0.0.1/fte table. Calculates FTE information for staff members. 
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

    return render_template('index.html', sql_table = table.log, table_title=table.col_names, table_name = table_name)


# Custom Query page - allow for custom SQL queries (for input sanitazation proof of concept)
@app.route('/admin', methods = ["GET", "POST"]) 
def admin():
    # Regex phrase containing "bad" SQL commands
    badwords = r'(?i)\b(?:DROP|DELETE|TRUNCATE|INSERT|UPDATE|ALTER|CREATE|SET)\b'
    if request.method == "POST":
        query = request.form.get("sql_query")
        print(query)
        # Error checking statements
        # Prevent Query from containing bad SQL commands
        if bool(re.search(badwords, query)):
            error = "You've entered a forbidden query! DROP, TRUNCATE, DELETE not allowed."
            return render_template('admin.html', error = error)
        elif query == "":
            error = "Query can not be empty."
            return render_template('admin.html', error = error)
        else:
            table = DataTable(query)
            # Currently DataTable class returns a "0" if SQL query is invalid (try/except clause)
            if(table.log == 0):
                error = "Query error, or table or data may not exist."
                return render_template('admin.html', error = error)
            # Finally, if no errors, output custom query
            return render_template('admin.html', sql_table = table.log, table_title=table.col_names)
    return render_template('admin.html')



# Main loop.
if __name__ == "__main__":
    app.run('127.0.0.1')