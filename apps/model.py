from flask_security import UserMixin , RoleMixin

from apps import db


class Role(db.Model , RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer() , primary_key=True)
    name = db.Column(db.String(80) , unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model , UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(255) , unique=True)
    email = db.Column(db.String(255) , unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    role = db.Column(db.Integer , db.ForeignKey('role.id'))
    role_r = db.relationship("Role" , backref=db.backref('users' , lazy='dynamic'))

    # def __init__(self , name , email , password , active):
    #     self.name = name
    #     self.email = email
    #     self.password = password
    #     self.active = active

    def __str__(self):
        return self.name


class Customer(db.Model , UserMixin):
    __tablename__ = 'customer'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(225) , unique=True)
    sex = db.Column(db.String(255))
    hcondition = db.Column(db.String(255) , nullable=True)
    adress = db.Column(db.String(255) , nullable=True)
    sid = db.Column(db.String(255) , unique=True)
    phoneNumber = db.Column(db.String(255) , unique=True)
    time = db.Column(db.DateTime)

    def __init__(self , id , name , sex , hcondition , adress , sid , phoneNumber , time):
        self.id = id
        self.name = name
        self.sex = sex
        self.hcondition = hcondition
        self.adress = adress
        self.sid = sid
        self.phoneNumber = phoneNumber
        self.time = time

    def __repr__(self):
        return '<User %r>' % self.name


class Coach(db.Model):
    # __tablename__ = "coach"
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    sid = db.Column(db.String(255) , unique=True)
    nation = db.Column(db.String(255))
    political = db.Column(db.String(255))
    education = db.Column(db.String(255))
    phoneNumber = db.Column(db.String(255) , unique=True)
    job = db.Column(db.String(255) , nullable=True)
    school = db.Column(db.String(255) , nullable=True)
    otherData = db.Column(db.String(255))
    lessons = db.relationship('Lesson' , backref="Coach")

    #
    # def __init__(self , id , name , sex , sid , nation , political , education , phoneNumber , job , school ,
    #              otherData):
    #     self.id = id
    #     self.name = name
    #     self.sex = sex
    #     self.sid = sid
    #     self.nation = nation
    #     self.political = political
    #     self.education = education
    #     self.phoneNumber = phoneNumber
    #     self.job = job
    #     self.school = school
    #     self.otherData = otherData

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Lesson(db.Model):
    __tablename__ = "lesson"
    id = db.Column(db.Integer , primary_key=True)
    lessonName = db.Column(db.String(255))
    lessonData = db.Column(db.String(255))
    lessonTime = db.Column(db.DateTime)
    room = db.Column(db.String(255))
    cost = db.Column(db.DECIMAL)
    coach = db.Column(db.Integer , db.ForeignKey('coach.id'))

    # def __init__(self , id , lessonData , lessonTime , room , coach , cost):
    #     self.id = id
    #     self.lessonData = lessonData
    #     self.lessonTime = lessonTime
    #     self.room = room
    #     self.coach = coach
    #     self.cost = cost
    def __str__(self):
        return self.lessonName

    def __unicode__(self):
        return self.name
