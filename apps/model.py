from flask_security import UserMixin , RoleMixin

from apps import db

roles_users = db.Table('roles_users' ,
                       db.Column('user_id' , db.Integer() , db.ForeignKey('user.id')) ,
                       db.Column('role_id' , db.Integer() , db.ForeignKey('role.id')))


class Role(db.Model , RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer() , primary_key=True)
    name = db.Column(db.String(80) , unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class User(db.Model , UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(255) , unique=True)
    email = db.Column(db.String(255) , unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role' , secondary=roles_users ,
                            backref=db.backref('users' , lazy='dynamic'))

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


lessons_of_customer = db.Table('lessons_of_customer' ,
                               db.Column('lesson_id' , db.Integer() , db.ForeignKey('lesson.id')) ,
                               db.Column('customer_id' , db.Integer() , db.ForeignKey('customer.id')))


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(225) , unique=True)
    sex = db.Column(db.String(255))
    hcondition = db.Column(db.String(255) , nullable=True)
    adress = db.Column(db.String(255) , nullable=True)
    sid = db.Column(db.String(255) , unique=True)
    phoneNumber = db.Column(db.String(255) , unique=True)
    time = db.Column(db.DateTime)
    money = db.Column(db.DECIMAL)
    cards = db.relationship("VipCard" , backref='customers')
    lessons = db.relationship('Lesson' , secondary=lessons_of_customer ,
                              backref=db.backref('customers' , lazy='dynamic'))

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class VipCard(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(255) , unique=True)
    available_Times = db.Column(db.Integer)
    overdue_Date = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    discount = db.Column(db.DECIMAL(10 , 2))
    saled = db.Column(db.Boolean)
    customer = db.Column(db.Integer , db.ForeignKey('customer.id'))

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Coach(db.Model):
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

    def __str__(self):
        return self.lessonName

    def __unicode__(self):
        return self.lessonName


class Consuming(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    customerid = db.Column(db.Integer , db.ForeignKey('customer.id'))
    goodstype = db.Column(db.String(255))
    goodsid = db.Column(db.Integer)
    time = db.Column(db.DateTime)


class Leave(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    customerid = db.Column(db.Integer , db.ForeignKey('customer.id'))
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)
