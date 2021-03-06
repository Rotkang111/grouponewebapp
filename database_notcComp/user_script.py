from crypt import methods
from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Create a Flask Instance
app = Flask(__name__)
#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#Secret Key
app.config['SECRET_KEY'] = "my super secret key"
# Initialize The Database
db = SQLAlchemy(app)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create A string
    def __repr__(self):
        return "name: {}: email: {}: date added{}".format(self.name, self.email, self.date_added)

 
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
@app.route("/login")
def login():
    return render_template('login.html')

#Registration page
@app.route("/register")
def register():
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