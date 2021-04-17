from flask import Flask
from flask_restplus import Api, Resource, fields,marshal
from werkzeug.contrib.fixers import ProxyFix
from db import db
from model.student import StudentModel, StudentDAO
from model.degree import DegreeModel, DegreeDAO

# App definition.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:akan@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.before_first_request
def create_tables():
    db.create_all()

# Api definition.
api = Api(app, version='1.0', title='Student API',
    description='A simple Student API',
)






ns = api.namespace('students', description='Student operations')
degree_ns = api.namespace('degrees', description='Degree operations')

degree = api.model('Degree', {
    'id': fields.Integer(readOnly=True, description='students unique identifier'),
    'name': fields.String(required=True, description='student name '),
    'degree_id': fields.Integer(required=True, description='Degree Id'),
    'year': fields.Integer(required=True, description='year of degree'),
    'student_id':fields.Integer
})

student = api.model('Student', {
    'id': fields.Integer(readOnly=True, description='students unique identifier'),
    'name': fields.String(required=True, description='student name '),
    'registration_no': fields.Integer(required=True, description='student Registration Number'),
    'year': fields.Integer(required=True, description='year of degree'),
    #'degree':fields.List(fields.Nasted(degree))
})

DAO = StudentDAO()
DAO1 = DegreeDAO()


@ns.route('/')
class StudentList(Resource):
    @ns.doc('list_students')
    @ns.marshal_list_with(student)
    def get(self):
        '''List all tasks'''
        return DAO.students

    @ns.doc('create_student')
    @ns.expect(student)
    @ns.marshal_with(student, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Student not found')
@ns.param('id', 'The Student identifier')
class Student(Resource):
    '''Show a single student item and lets you delete them'''
    @ns.doc('get_student')
    @ns.marshal_with(student)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_student')
    @ns.response(204, 'student deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(student)
    @ns.marshal_with(student)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)
        
@degree_ns.route('/')
class DegreeList(Resource):
    @ns.doc('list_degrees')
    @ns.marshal_list_with(degree)
    def get(self):
        '''List all tasks'''
        return DAO1.degrees

    @degree_ns.doc('create_degree')
    @degree_ns.expect(degree)
    @degree_ns.marshal_with(degree, code=201)
    def post(self):
        '''Create a new task'''
        return DAO1.create(api.payload), 201


@degree_ns.route('/<int:id>')
@degree_ns.response(404, 'Degreet not found')
@degree_ns.param('id', 'The Degree identifier')
class Degree(Resource):
    '''Show a single student item and lets you delete them'''
    @degree_ns.doc('get_degree')
    @degree_ns.marshal_with(degree)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO1.get(id)

    @degree_ns.doc('delete_degree')
    @degree_ns.response(204, 'degree deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO1.delete(id)
        return '', 204

    @degree_ns.expect(degree)
    @degree_ns.marshal_with(degree)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO1.update(id, api.payload)






if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
