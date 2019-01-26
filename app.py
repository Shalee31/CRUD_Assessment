""" importing required modules """
import uuid
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# initializing a variable of Flask
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@127.0.0.1:3306/db1'
APP.config['SECRET_KEY'] = 'shalini'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

DB = SQLAlchemy(APP)


class Student(DB.Model):  # pylint: disable=too-few-public-methods
    """ Creating student table """
    student_id = DB.Column('id', DB.String(100), primary_key=True, nullable=False)
    student_name = DB.Column(DB.String(100))
    # Adding foreign key reference to class
    class_id = DB.Column(DB.String(100), DB.ForeignKey('classes.id'))
    classes = DB.relationship("Classes", foreign_keys='Classes.class_leader')
    created_on = DB.Column(DB.DateTime(), server_default=DB.func.now())
    updated_on = DB.Column(DB.DateTime(), server_default=DB.func.now())

    def __init__(self, student_id, student_name, class_id):
        self.student_id = student_id
        self.student_name = student_name
        self.class_id = class_id


class Classes(DB.Model):  # pylint: disable=too-few-public-methods
    """ Creating table class """
    class_id = DB.Column('id', DB.String(100), primary_key=True)
    class_name = DB.Column(DB.String(100))
    # Creating relationship with student entity
    student = DB.relationship("Student", foreign_keys='Student.class_id')
    class_leader = DB.Column(DB.String(100), DB.ForeignKey('student.id'))
    created_on = DB.Column(DB.DateTime(), server_default=DB.func.now())
    updated_on = DB.Column(DB.DateTime(), server_default=DB.func.now())

    def __init__(self, class_id, class_name):
        self.class_id = class_id
        self.class_name = class_name


@APP.route('/')
def index():
    """ index function with route to home page with all student's list """
    data = DB.session.query(Student, Classes).filter(Student.class_id == Classes.class_id).all()
    return render_template('home.html', data=data)


@APP.route('/add_student')
def add_student():
    """ add_student function with route to add_student page """
    return render_template('add_student.html', class_details=Classes.query.all())


@APP.route('/add_class')
def add_class():
    """ add_class function with route to add_class page """
    return render_template('add_class.html')


@APP.route('/view/<string:s_id>')
def view(s_id):
    """ view function with route to page displaying particular student details """
    data = DB.session.query(Student, Classes).filter\
        (Student.class_id == Classes.class_id).filter(Student.student_id == s_id).all()
    return render_template('view.html', data=data)


@APP.route('/edit/<string:s_id>')
def edit(s_id):
    """ edit function with route to page allowing updation of particular student details """
    data = DB.session.query(Student, Classes).filter(Student.class_id == Classes.class_id).filter(
        Student.student_id == s_id).all()
    return render_template('edit.html', data=data, class_details=Classes.query.all())


@APP.route('/delete/<string:s_id>')
def delete(s_id):
    """ delete function with route to page allowing deletion of particular student details """
    student = Student.query.filter_by(student_id=s_id).first()
    class_details = Classes.query.filter_by(class_id=student.class_id).first()

    if class_details.class_leader == student.student_id:
        flash('Student record cannot be deleted. Please select a new class leader before deleting.')
    else:
        DB.session.delete(student)
        DB.session.commit()
        flash('Student record deleted Successfully!')
    return redirect(url_for('index'))


@APP.route('/db_edit', methods=['POST'])
def db_edit():
    """ DB_edit function to save student's updates details """
    if request.method == 'POST':
        if not request.form['student_name']:
            flash('Please enter all fields', 'error')
        else:
            s_id = request.form['student_id']
            class_leader = request.form['class_leader']
            student = Student.query.filter_by(student_id=s_id).first()
            class_details = Classes.query.filter_by(class_id=student.class_id).first()

            if class_leader == 'Yes' and class_details.class_leader != s_id:
                student.student_name = request.form['student_name']
                student.class_id = request.form['class_id']
                student.updated_on = DB.func.now()

                class_details.class_leader = student.student_id
                class_details.updated_on = student.updated_on

                DB.session.commit()
                flash('Student record updated successfully.')
            elif class_leader == 'No' and class_details.class_leader == s_id:
                student.student_name = request.form['student_name']
                student.class_id = request.form['class_id']
                student.updated_on = DB.func.now()

                class_details.class_leader = None
                class_details.updated_on = student.updated_on

                DB.session.commit()
                flash('Student record updated successfully.')
            else:
                student.student_name = request.form['student_name']
                student.class_id = request.form['class_id']
                student.updated_on = DB.func.now()

                DB.session.commit()
                flash('Student record updated successfully.')
        return redirect(url_for('index'))
    return redirect(url_for('edit'))


@APP.route('/db_student', methods=["GET", "POST"])
def db_student():
    """ DB_student function to save student's details """
    if request.method == 'POST':
        if not request.form['student_name']:
            flash('Please enter all fields', 'error')
        else:
            class_leader = request.form['class_leader']
            if class_leader == 'Yes':
                student_id = uuid.uuid1()
                student = Student(student_id.int, request.form['student_name'],\
                                  request.form['class_id'])
                class_details = Classes.query.filter_by(class_id=request.form['class_id']).first()
                DB.session.add(student)
                DB.session.commit()

                class_details.class_leader = student.student_id
                class_details.updated_on = DB.func.now()
                DB.session.add(class_details)
                DB.session.commit()
                flash('Student record saved successfully.')
            else:
                student_id = uuid.uuid1()
                student = Student(student_id.int, request.form['student_name'],\
                                  request.form['class_id'])
                DB.session.add(student)
                DB.session.commit()
                flash('Student record saved successfully.')
        return redirect(url_for('index'))
    return redirect(url_for('add_student'))


@APP.route('/db_class', methods=["GET", "POST"])
def db_class():
    """ DB_class function to save class' details """
    if request.method == 'POST':
        class_id = uuid.uuid1()
        class_info = Classes(class_id.int, request.form['class_name'])
        DB.session.add(class_info)
        DB.session.commit()
    flash('Class record saved successfully.')
    return redirect(url_for('index'))


if __name__ == "__main__":
    DB.create_all()
    APP.run(debug=True)
