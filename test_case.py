import pytest
import app
from app import *
from flask.testing import FlaskClient
import flask

# Connection to the database
APP = Flask(__name__)
APP.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:12345@127.0.0.1:3306/db1'
APP.config['SECRET_KEY'] = "shalini"
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
DB = SQLAlchemy(APP)


@pytest.fixture(scope='module')
def test_resp_code():
    client = app.APPL.test_client()
    return client


def test_home(test_resp_code):
    resp = test_resp_code.post('/')
    assert resp.status_code == 200


dict_new_student = {"student_name": "Shalini", "class_id": "11624370275509396860417412588704679245", "class_leader": "Yes"}
dict_new_student2 = {"student_name": "Shirley", "class_id": "4112487526877323080716225628316419405", "class_leader": "No"}

dict_new_class = {"class_name": "TE CMPN A"}

dict_update = {"student_id": "150885054602642764855231074050694759757", "student_name": "Lara",
               "class_id": "4112487526877323080716225628316419405", "class_leader": "Yes"}
dict_update2 = {"student_id": "150885054602642764855231074050694759757", "student_name": "Lara",
                "class_id": "4112487526877323080716225628316419405", "class_leader": "No"}


def test_new_student(test_resp_code):
    resp = test_resp_code.post('/db_student', data=dict_new_student)
    assert resp.status_code == 302


def test_new_class(test_resp_code):
    resp = test_resp_code.post('/db_class', data=dict_new_class)
    assert resp.status_code == 302


def test_update_rec(test_resp_code):
    resp = test_resp_code.post('/db_edit', data=dict_update)
    assert resp.status_code == 302

	
def test_update_rec2(test_resp_code):
    resp = test_resp_code.post('/db_edit', data=dict_update2)
    assert resp.status_code == 302


def test_new_student2(test_resp_code):
    resp = test_resp_code.post('/db_student', data=dict_new_student2)
    assert resp.status_code == 302