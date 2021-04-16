from db import db

class StudentModel(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    registration_no =db.Column(db.Integer,nullable=False)
    year = db.Column(db.Integer,nullable=False)    
    student = db.relationship("DegreeModel", back_populates="degree")

    def __init__(self, name,registration_no,year):
        self.name = name,
        self.registration_no = registration_no,
        self.year=year

    def __repr__(self):
        return 'StudentModel(name=%s,registration_no=%s,year=%s)' % (self.name,self.registration_no,self.year)

class StudentDAO(object):
    
    @property
    def students(self):
        return StudentModel.query.all()

    def get(self, id):
        student = StudentModel.query.filter_by(id=id).first()
        if student:
            return {"id": student.id, "name": student.name,"registration_no":student.registration_no,"year":student.year}
        else: print('Student not found')

    def create(self, data):
        student = StudentModel(data['name'],data['registration_no'],data['year'])      
        db.session.add(student)
        db.session.commit()
        return student

    def update(self, id, data):
        student = StudentModel.query.filter_by(id=id).first()
        student.name = data['name'],
        student.registration_no=data['registration_no'],
        student.year=data['year']
        db.session.commit()
        return student

    def delete(self, id):
        student = StudentModel.query.filter_by(id=id).first()
        db.session.delete(student)
        db.session.commit()