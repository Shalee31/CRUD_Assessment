# importing flask modules
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import uuid

# initializing a variable of Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@127.0.0.1:3306/db1'
app.config['SECRET_KEY'] = 'shalini'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


# Creating student table
class Student(db.Model):
    student_id = db.Column('id', db.String(100), primary_key=True, nullable=False)
    student_name = db.Column(db.String(100))
    # Adding foreign key reference to class
    class_id = db.Column(db.String(100), db.ForeignKey('classes.id'))
    classes = db.relationship("Classes", foreign_keys='Classes.class_leader')
    created_on = db.Column(db.DateTime(), server_default=db.func.now())
    updated_on = db.Column(db.DateTime(), server_default=db.func.now())

    def __init__(self, student_id, student_name, class_id):
        self.student_id = student_id
        self.student_name = student_name
        self.class_id = class_id


# Creating table class
class Classes(db.Model):
    class_id = db.Column('id', db.String(100), primary_key=True)
    class_name = db.Column(db.String(100))
    # Creating relationship with student entity
    student = db.relationship("Student", foreign_keys='Student.class_id')
    class_leader = db.Column(db.String(100), db.ForeignKey('student.id'))
    created_on = db.Column(db.DateTime(), server_default=db.func.now())
    updated_on = db.Column(db.DateTime(), server_default=db.func.now())

    def __init__(self, class_id, class_name):
        self.class_id = class_id
        self.class_name = class_name


# index function with route to home page with all student's list
@app.route('/')
def index():
    data = db.session.query(Student, Classes).filter(Student.class_id == Classes.class_id).all()
    return render_template('home.html', data=data)


# add_student function with route to add_student page
@app.route('/add_student')
def add_student():
    return render_template('add_student.html', class_details=Classes.query.all())


# add_class function with route to add_class page
@app.route('/add_class')
def add_class():
    return render_template('add_class.html')


# view function with route to page displaying particular student details
@app.route('/view/<string:id>')
def view(id):
    data = db.session.query(Student, Classes).filter(Student.class_id == Classes.class_id).filter(Student.student_id == id).all()
    return render_template('view.html', data=data)


# edit function with route to page allowing updation of particular student details
@app.route('/edit/<string:id>')
def edit(id):
    data = db.session.query(Student, Classes).filter(Student.class_id == Classes.class_id).filter(
        Student.student_id == id).all()
    return render_template('edit.html', data=data, class_details=Classes.query.all())


# delete function with route to page allowing deletion of particular student details
@app.route('/delete/<string:id>')
def delete(id):
    student = Student.query.filter_by(student_id=id).first()
    class_details = Classes.query.filter_by(class_id=student.class_id).first()

    if class_details.class_leader == student.student_id:
        flash('Student record cannot be deleted. Please select a new class leader before deleting.')
    else:
        db.session.delete(student)
        db.session.commit()
        flash('Student record deleted Successfully!')
    return redirect(url_for('index'))


# db_edit function to save student's updates details
@app.route('/db_edit', methods=['POST'])
def db_edit():
    if request.method == 'POST':
        if not request.form['student_name']:
            flash('Please enter all fields', 'error')
        else:
            id = request.form['student_id']
            class_leader = request.form['class_leader']
            student = Student.query.filter_by(student_id=id).first()
            class_details = Classes.query.filter_by(class_id=student.class_id).first()

            if class_leader == 'Yes' and class_details.class_leader != id:
                student.student_name = request.form['student_name']
                student.class_id = request.form['class_id']
                student.updated_on = db.func.now()

                class_details.class_leader = student.student_id
                class_details.updated_on = student.updated_on

                db.session.commit()
                flash('Student record updated successfully.')
            elif class_leader == 'No' and class_details.class_leader == id:
                student.student_name = request.form['student_name']
                student.class_id = request.form['class_id']
                student.updated_on = db.func.now()

                class_details.class_leader = None
                class_details.updated_on = student.updated_on

                db.session.commit()
                flash('Student record updated successfully.')
            else:
                print(".......")
                student.student_name = request.form['student_name']
                student.class_id = request.form['class_id']
                student.updated_on = db.func.now()

                db.session.commit()
                flash('Student record updated successfully.')
        return redirect(url_for('index'))
    return redirect(url_for('edit'))


# db_student function to save student's details
@app.route('/db_student', methods=["GET", "POST"])
def db_student():
    if request.method == 'POST':
        if not request.form['student_name']:
            flash('Please enter all fields', 'error')
        else:
            class_leader = request.form['class_leader']
            if class_leader == 'Yes':
                student_id = uuid.uuid1()
                student = Student(student_id.int, request.form['student_name'], request.form['class_id'])
                class_details = Classes.query.filter_by(class_id=request.form['class_id']).first()
                db.session.add(student)
                db.session.commit()

                class_details.class_leader = student.student_id
                class_details.updated_on = db.func.now()
                db.session.add(class_details)
                db.session.commit()
                flash('Student record saved successfully.')
            else:
                student_id = uuid.uuid1()
                student = Student(student_id.int, request.form['student_name'], request.form['class_id'])
                db.session.add(student)
                db.session.commit()
                flash('Student record saved successfully.')
        return redirect(url_for('index'))
    return redirect(url_for('add_student'))


# db_class function to save class' details
@app.route('/db_class', methods=["GET", "POST"])
def db_class():
    if request.method == 'POST':
        uid_id = uuid.uuid1()
        class_info = Classes(uid_id.int, request.form['class_name'])
        db.session.add(class_info)
        db.session.commit()
    flash('Class record saved successfully.')
    return redirect(url_for('index'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
