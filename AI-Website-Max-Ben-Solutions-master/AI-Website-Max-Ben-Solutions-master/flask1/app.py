#https://github.com/PacktPublishing/The-Ultimate-Flask-Course/tree/master/Section%2018
from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
#### upload download

import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader, PdfFileWriter
#win10 \ unix /
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '\\new_uploads\\'
print(UPLOAD_FOLDER)
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '\\downloads\\'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size upto 8mb
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


############
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

#UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
############

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(path, filename):
    remove_watermark(path, filename)
    with open(path, 'a') as f:
       f.write("\nAdded processed content")


def remove_watermark(path, filename):
    print('in remove_watermark....')
    input_file = PdfFileReader(open(path, 'rb'))
    output = PdfFileWriter()
    for page_number in range(input_file.getNumPages()):
        page = input_file.getPage(page_number)
        page.mediaBox.lowerLeft = (page.mediaBox.getLowerLeft_x(), 20)
        output.addPage(page)
#    output_stream = open(app.config['DOWNLOAD_FOLDER'] + filename, 'wb')
    output_stream = open(DOWNLOAD_FOLDER + filename, 'wb')
    output.write(output_stream)

@app.route('/updown/<filename>')
def uploaded_file(filename):
   return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

#g is for global storage... 
import os
import sqlite3
app = Flask(__name__)

app.config['DEBUG'] = True  #config debug
app.config['SECRET_KEY'] = 'Thisisasecret'

def connect_db():
    sql = sqlite3.connect(r'C:\Users\i080272\PycharmProjects\IDEA1\data.db')
    sql.row_factory = sqlite3.Row  #dict instead of tuples
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db   #stores in g

@app.teardown_appcontext
def close_db(error):  #close down db
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


## example of df to html
# https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table
import pandas as pd


@app.route('/df')
def df():
    df = pd.DataFrame({'col1': ['abc', 'def', 'tre'],
                       'col2': ['foo', 'bar', 'stuff']})
    return df.to_html(header="true", table_id="table")

##check boxes to select columns
#https://stackoverflow.com/questions/31859903/get-the-value-of-a-checkbox-in-flask

##file upload
#https://www.tutorialspoint.com/flask/flask_file_uploading.htm
#https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
#https://www.javatpoint.com/flask-file-uploading
#https://pythonise.com/series/learning-flask/flask-uploading-files



@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()  #set of dictionaries 
    return 'the id {} name {} the location is {}'.format(results[1]['id'],
                                                         results[1]['name'],
                                                         results[1]['location'])
    
@app.route("/")
def index():
    return '''<H1>Learning app.py </H1>
                <h2>/home jinja demo page with vars </h2>
                <h2>/process for submit POST and GET </h2>
                <h2>/query for name and location passing</h2>
                <h2>/goodbye for simple message</h2>
                <h2>/theform for db users insert example </h2>
                <h2>/df for example of df to html </h2>                
                <h2>/viewresults for database record</h2>
                <h2>/checkbox for checkbox test</h2>
                <h2>/simpleupload - simple upload version </h2>
                <h2>/updown - upload - process -download </h2>
                '''
#https://www.youtube.com/watch?v=_sgVt16Q4O4
@app.route("/checkbox", methods=['GET','POST'])
def checkbox():
    if request.method=='POST':
        request.form.get('mycheckbox')
        print(request.form.getlist('mycheckbox') )
        print('...................')
        return 'Done!'
    return render_template('checkbox.html')


@app.route("/updown", methods=['GET', 'POST'])
def updown():
   if request.method == 'POST':
       if 'file' not in request.files:
           print('No file attached in request')
           return redirect(request.url)
       file = request.files['file']
       if file.filename == '':
           print('No file selected')
           return redirect(request.url)
       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           # process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
           # return redirect(url_for('uploaded_file', filename=filename))

           file.save(os.path.join(UPLOAD_FOLDER, filename))
           process_file(os.path.join(UPLOAD_FOLDER, filename), filename)
           return redirect(url_for('return_files_tut', filename=filename))
#           return redirect(url_for('uploaded_file', filename=filename))


   return render_template('updown.html')

@app.route('/down/<filename>')
def down(filename):
#   return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)
   #return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True, attachment_filename='')


@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER #+ filename
#    return send_from_directory(file_path, filename, as_attachment=True, attachment_filename='')
#    return send_from_directory(file_path, filename, attachment_filename='x.pdf' )
    #opens it no matter what - could be adobe pdf local setting? 
    return send_from_directory(file_path, filename, attachment_filename='x.pdf' ) #doesnt matter?


#https://www.youtube.com/watch?v=Y82XKGKUtrU&list=UUVyHIv1YB6eC2sR4QRSsMRQ&index=50
@app.route("/simpleupload", methods=['POST','GET'])
def simpleupload():
    if request.method=="POST":
        file = request.files['file']  #from the html
        file.save(os.path.join("uploads", file.filename))
        return render_template("simpleupload.html", message="1 It has been uploaded...maybe")
    return render_template("simpleupload.html", message="2 Please enter a file ")

#upload, process, download https://viveksb007.wordpress.com/2018/04/07/uploading-processing-and-downloading-files-in-flask/
#tbd...



@app.route("/goodbye")
def goodbye():
    return 'running away!'

@app.route("/query")
def query( ):
    name = request.args.get('name')
    location = request.args.get('location')
    return 'query ... {} from {}'.format(name, location)

@app.route("/process", methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']
    return 'welcome {} from {} '.format(name, location)

@app.route("/home1", methods =['GET','POST'], defaults={'name': 'Default'})
@app.route("/home1/<string:name>", methods=['POST','GET'])
def home1(name):
    return 'home1 welcome {} home from {}!'.format(name)


@app.route("/home",methods =['GET','POST'], defaults={'name': 'Default'})
@app.route("/home/<string:name>", methods=['POST','GET'])
def home(name):
    session['name'] =name
    return render_template('home.html', name= name, display=True, mylist=[1,2,3,4],
                           dicts =[{'name':'zack'}, {'name':'zooey'}] )
#    return 'welcome home! {}'.format(name) #moved to template...

@app.route("/home_db",methods =['GET','POST'], defaults={'name': 'Default'})
@app.route("/home_db/<string:name>", methods=['POST','GET'])
def home_db(name):
    session['name'] =name
    db = get_db()
    cur = db.execute('select id,name,location from users')
    results = cur.fetchall()  #modify home.html to show results
    return render_template('home.html', name= name, display=True, mylist=[1,2,3,4],
                           dicts =[{'name':'zack'}, {'name':'zooey'}], results=results  ) #needed to pass results
#    return 'welcome home! {}'.format(name) #moved to template...

@app.route('/theform2', methods=['GET', 'POST'])
def theform2():

    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)', [name, location])
        db.commit()

        #return '<h1>Hello {}. You are from {}. You have submitted the form successfully!<h1>'.format(name, location)
        return redirect(url_for('home', name=name, location=location))



@app.route("/theform", methods=['GET','POST'])
def theform():
    if request.method == 'GET':
        # return '''<form method='POST' action='/process'>
        #       <input type = "text" name="name">
        #       <input type ="text" name="location">
        #       <input type="submit" name="Submit" > '''
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']
        
        db = get_db()
        db.execute('INSERT INTO users (name, location) values (?,?)',[name,location])
        db.commit()
        
        # return 'welcome {} from {} '.format(name, location)
        return redirect(url_for('home1', name=name))

@app.route("/form")
def form():
    return '''<form method='POST' action='/process'>
              <input type = "text" name="name">
              <input type ="text" name="location">
              <input type="submit" name="Submit" > '''

@app.route("/json")
def json():
    if 'name' not in session:
        name = 'oops '
    name = session['name']
    return jsonify({'key': 'value1', 'key12':[1,34,3],'name':name})

@app.route("/home/<name>" , defaults={'name':'Tacitus'})
@app.route("/home/<name>") #dynamic paths... int
def hello(name):
    return 'Hello ...'+name



if __name__ == '__main__':
#    port = int(os.environ.get('PORT',5000))
#    print(port)
    print('Running this on PORT 7000')
    app.run(host='127.0.0.1', port=7000, debug=True)