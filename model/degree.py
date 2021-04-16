from db import db

class DegreeModel(db.Model):
    __tablename__="degrees"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    degree_id =db.Column(db.Integer,nullable=False, unique=True)
    year = db.Column(db.Integer,nullable=False)
    student_id =db.Column(db.Integer,db.ForeignKey('students.id'))
    degree= db.relationship("StudentModel", back_populates="student")

    def __init__(self, name,degree_id,year,student_id):
        self.name = name,
        self.degree_id = degree_id,
        self.year=year,
        self.student_id=student_id

    def __repr__(self):
        return 'DegreeModel(name=%s,degree_id=%s,year=%s,student_id=%s)' % (self.name,self.degree_id,self.year,self.student_id)

class DegreeDAO(object):
    
    @property
    def degrees(self):
        return DegreeModel.query.all()

    def get(self, id):
        degree = DegreeModel.query.filter_by(id=id).first()
        if degree:
            return {"id": degree.id, "name": degree.name,"degree_id":degree.degree_id,"year":degree.year,"student_id":degree.student_id}
        else: print('Degree not found')

    def create(self, data):
        degree = DegreeModel(data['name'],data['degree_id'],data['year'],data['student_id'])      
        db.session.add(degree)
        db.session.commit()
        return degree

    def update(self, id, data):
        degree = DegreeModel.query.filter_by(id=id).first()
        degree.name = data['name'],
        degree.degree_id=data['degree_id'],
        degree.year=data['year']
        degree.year=data[student_id]
        db.session.commit()
        return degree

    def delete(self, id):
        degree = DegreeModel.query.filter_by(id=id).first()
        db.session.delete(degree)
        db.session.commit()