from crypt import methods
from flask import*
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///group1.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(11), nullable=False)
 
    
    def __init__(self, name, email, phone, password):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
      
    
# @app.route('/')
# def  show_all():
  
#     return render_template('show_all.html', students = students.query.all())
    
            

#Form Class
class NamerForm(FlaskForm):
    name = StringField('Enter full name', validators=[DataRequired()])
    submit = SubmitField('View Record')

            




#Home page
@app.route("/")
def index():
    return render_template('index.html')

#about page
@app.route("/about")
def about():
    return render_template('about.html')

#Contact page
@app.route("/contact")
def contact():
    return render_template('contact.html')

#Login page
@app.route("/login", methods = ["GET", "POST"])
def login():

    if request.method == "POST":
        curs = conn.cursor()
        connection=sqlite3.connect('group1.sqlite3')
        email = request.form['email']
        password = request.form['password']
        query = "SELECT email,password FROM users where email = 'email' and password = 'password'"
        curs.execute(query)
        results= curs.fetchall()

        if len(results)==0:
            flash("incorrect details, Try again")
        else:
            return redirect(url_for('index'))
    return render_template('login.html')

# #Registration page
# @app.route("/register")
# def register():
#     return render_template('register.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():    
    if request.method =='POST':                            
        if not request.form['name'] or not request.form['email'] or not request.form['phone'] or not request.form['password']:
            flash('Please enter all the fields', 'error')
        else:
            student = students(request.form['name'], request.form['email'], request.form['phone'], request.form['password'])
            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('index'))
    return render_template('register.html')

#Services page
@app.route("/services")
def services():
    return render_template('services.html')

#Database page
@app.route('/user', methods=['GET', 'POST'])
def user():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    return render_template('user.html',
    name = name,
    form = form)

#Internal error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404 





if __name__ == "__main__":
    app.run(debug = True)