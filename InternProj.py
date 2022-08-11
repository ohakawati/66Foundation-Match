from unicodedata import name
from flask import Flask, render_template,request
import PersonClass
from csv import writer
import average
import bq
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'Proj/Upload_folder/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Person = PersonClass.Person("","","","","","","","","","","","","")

# Returns Home page
@app.route('/',methods = ["POST", "GET"])
def index():
    return render_template('index.html')

# Returns skintype page and saves user name to person class
@app.route('/getStarted',methods = ["POST", "GET"])
def account():
    output = request.form.to_dict()
    Person.name = output["name"]
    Person.price = output["price"]

    return render_template('getStarted.html')

# Returns jewlery page and saves skintype to person class
@app.route('/clickedSkin',methods = ["POST", "GET"])
def skinType():
    Person.skintype = request.form["skin"]
    return render_template('jewlery.html')

# Returns coverage page and saves jewlery to person class
@app.route('/clickedJewlery',methods = ["POST", "GET"])
def jewleryType():
    Person.undertone = request.form["jewlery"]
    return render_template('coverage.html')

# Returns finish page and saves coverage to person class
@app.route('/clickedCoverage',methods = ["POST", "GET"])
def coverageType():
    Person.coverage = request.form["coverage"]
    return render_template('finish.html')

# Returns upload page and save finish to person class
@app.route('/clickedFinish',methods = ["POST", "GET"])
def finishType():
    Person.finish = request.form["finish"]
    return render_template('upload.html')

# Returns loading page and save uploaded images and data gets saved to csv
@app.route('/uploadedImg',methods = ["POST", "GET"])
def uploadedImg():

    if request.method == 'POST':
        f = request.files['img1']
        f.save(secure_filename(f.filename))

        r = request.files['img2']
        r.save(secure_filename(r.filename))

        l = request.files['img3']
        l.save(secure_filename(l.filename))

        rgb = average.average_color(f.filename,r.filename,l.filename)
    name = Person.name
    if Person.finish == "Matte":
        Person.foundation = bq.query_matte(rgb[0], rgb[1], rgb[2], Person.undertone, Person.coverage, Person.price)
    else:
        Person.foundation = bq.query_dewy(rgb[0], rgb[1], rgb[2], Person.undertone, Person.coverage, Person.price)
    
    data = bq.get_data(Person.foundation)

    Person.brand = data[0]
    Person.link = data[1]
    Person.finalprice = data[2]

    list = [Person.name, Person.skintype, Person.undertone, Person.coverage, Person.finish, Person.price, rgb[0], rgb[1], rgb[2], Person.foundation, Person.brand, Person.link, Person.finalprice]
    with open('data.csv', 'a') as file:
        writer_object = writer(file)
        writer_object.writerow(list)
        file.close()

    return render_template('loading.html', name = name)

@app.route('/finalPage',methods = ["POST", "GET"])
def finalPage():
    foundation = Person.foundation
    brand = Person.brand
    link = Person.link
    finalprice = Person.finalprice

    return render_template('final.html', foundation = foundation, brand = brand, link = link, finalprice = finalprice)


if __name__ == "__main__":
    app.run(debug=True)