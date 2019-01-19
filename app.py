# importing flask modules
from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy

# initializing a variable of Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost:5000/db1'
app.config['SECRET_KEY'] = 'shalini'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# index function with route to home page with all student's list
@app.route('/')
def index():
    return render_template('home.html')


# add_student function with route to add_student page
@app.route('/add_student')
def add_student():
    return render_template('add_student.html')


# add_class function with route to add_class page
@app.route('/add_class')
def add_class():
    return render_template('add_class.html')


# view function with route to page displaying particular student details
@app.route('/view/<string:id>')
def view(id):
    return render_template('view.html')


# edit function with route to page allowing updation of particular student details
@app.route('/edit/<string:id>')
def edit(id):
    return render_template('edit.html')


# delete function with route to page allowing deletion of particular student details
@app.route('/delete/<string:id>')
def delete(id):
    flash('Student record deleted successfully.')
    return render_template('home.html')


# db_edit function to save student's updates details 
@app.route('/db_edit')
def db_edit():
    flash('Student record updated successfully.')
    return render_template('home.html')


# db_student function to save student's details 
@app.route('/db_student')
def db_student():
    flash('Student record saved successfully.')
    return render_template('home.html')


# db_class function to save class' details 
@app.route('/db_class')
def db_class():
    flash('Class record saved successfully.')
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
