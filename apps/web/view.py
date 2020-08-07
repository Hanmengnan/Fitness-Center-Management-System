from flask import url_for , redirect , render_template , request
from flask_admin import helpers as admin_helpers
from flask_security import login_required , login_user , logout_user , roles_required

from apps import admin
from . import web
import datetime


@web.context_processor
def web_context_processor():
    return dict(
        admin_base_template=admin.base_template ,
        admin_view=admin.index_view ,
        get_url=url_for ,
        h=admin_helpers
    )


@web.route("/")
def init():
    return redirect(url_for('web.index'))


@web.route("/admin")
def index():
    return render_template('admin/mybase.html')


from apps.web.forms import *
from apps.model import User
from apps import db , user_datastore
from apps.model import *


@web.route('/login' , methods=['POST' , 'GET'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is not None:
            if form.password.data == user.password:
                login_user(user)
                return redirect('/admin')

        return render_template('login/login.html' , form=form , m="用户名或密码错误")

    return render_template('login/login.html' , form=form , m="")


@web.route('/logout')
@login_required
def logout():
    logout_user()


@web.route('/register' , methods=['POST' , 'GET'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        re_password = form.re_password.data

        if password == re_password:
            role = user_datastore.find_role("user")
            user = user_datastore.create_user(name=username , email=email , password=password)
            user_datastore.add_role_to_user(user , role)
            db.session.commit()
            return redirect('/login')
        return render_template('login/register.html' , form=form , m="两次输入密码不一致")
    return render_template('login/register.html' , form=form , m="")


@web.route("/profile" , methods=['GET'])
def profile():
    from flask_security import current_user
    from apps.model import Customer
    userid = current_user.id
    customer = Customer.query.filter_by(id=userid).first()
    name = customer.name
    sex = customer.sex
    hcondition = customer.hcondition
    address = customer.adress
    sid = customer.sid
    phoneNumber = customer.phoneNumber
    money = customer.money

    return render_template('other/index.html' , **locals() , m="")


@web.route("/profile/<action>" , methods=['POST'])
def profileAction(action):
    from flask_security import current_user

    userid = current_user.id
    customer = Customer.query.filter_by(id=userid).first()
    name = customer.name
    sex = customer.sex
    hcondition = customer.hcondition
    address = customer.adress
    sid = customer.sid
    phoneNumber = customer.phoneNumber
    money = customer.money
    if action == "transferCard":
        cid = request.form.get("cardid")
        uid = request.form.get("userid")
        old_owner = VipCard.query.filter_by(customer=userid , id=cid).first()
        aim_customer = Customer.query.filter_by(id=uid).first()
        if aim_customer and old_owner:
            VipCard.query.filter_by(customer=userid , id=cid).update({"customer": int(uid)})
            db.session.commit()
            return render_template('other/index.html' , **locals() , m="操作成功")
        else:
            return render_template('other/index.html' , **locals() , m="操作失败")

    elif action == "leave":
        dayNum = request.form.get("dayNum")
        vipcards = VipCard.query.filter_by(customer=userid)
        for card in vipcards:
            date = card.overdue_Date + datetime.timedelta(days=int(dayNum))
            VipCard.query.filter_by(id=card.id).update({"overdue_Date": date})
        db.session.commit()
        return render_template('other/index.html' , **locals() , m="操作成功")

    elif action == "buyCard":
        cardid = request.form.get("cardid")
        card = VipCard.query.filter_by(id=cardid).first()
        if card != None:
            if customer.money >= card.price:
                if card.saled == True:
                    if card.customer == userid:
                        date = card.overdue_Date + datetime.timedelta(days=365)
                        VipCard.query.filter_by(id=card.id).update({"overdue_Date": date})
                        Customer.query.filter_by(id=userid).update({"money": customer.money - card.price})
                        db.session.commit()
                        return render_template('other/index.html' , **locals() , m="操作成功")
                    else:
                        return render_template('other/index.html' , **locals() , m="该卡为别人所有，不能购买")
                else:
                    VipCard.query.filter_by(id=card.id).update({"customer": userid , "saled": True})
                    Customer.query.filter_by(id=userid).update({"money": customer.money - card.price})
                    db.session.commit()
                    return render_template('other/index.html' , **locals() , m="操作成功")
            else:
                return render_template('other/index.html' , **locals() , m="金额不足")
        else:
            return render_template('other/index.html' , **locals() , m="卡号错误")

    elif action == "buyLesson":
        cardid = request.form.get("cardid")
        lessonid = request.form.get("lessonid")

        customer = Customer.query.filter_by(id=userid).first()
        card = VipCard.query.filter_by(id=cardid).first()
        lesson = Lesson.query.filter_by(id=lessonid).first()

        leave = Leave.query.filter_by(id=userid).first()
        if leave != None:
            if datetime.datetime.now() > leave.endtime:
                leave = Leave.query.filter_by(id=userid).delete()
            else:
                return render_template('other/index.html' , **locals() , m="请假期间不能消费 ")

        if card == None or card.customer != userid:
            return render_template('other/index.html' , **locals() , m="卡号错误")
        elif lesson == None:
            return render_template('other/index.html' , **locals() , m="课程号错误")
        else:
            r = (customer.money) - (lesson.cost * card.discount)
            if r < 0:
                return render_template('other/index.html' , **locals() , m="金额不足")
            else:
                Customer.query.filter_by(id=userid).update({"money": r})
                db.session.commit()
                return render_template('other/index.html' , **locals() , m="操作成功")
    else:
        return render_template('other/index.html' , **locals() , m="非法操作")


@web.route("/advanced/lesson" , methods=['GET' , 'POST'])
def advancedLesson():
    if request.method == "GET":
        return render_template('/other/lesson.html' , m="" , lessonList=[])
    else:
        betime = request.form.get("betime").split(" - ")
        start = datetime.datetime.strptime(betime[0] , "%m/%d/%Y")
        end = datetime.datetime.strptime(betime[1] , "%m/%d/%Y")
        Lessons = Lesson.query.filter(Lesson.lessonTime <= end).filter(Lesson.lessonTime >= start).all()
        LessonList = []
        for i in Lessons:
            LessonDict = {}
            LessonDict["lessonName"] = i.lessonName
            LessonDict["LessonData"] = i.lessonData
            LessonDict["lessonTime"] = i.lessonTime.strftime("%Y-%m-%d")
            LessonDict["lessonRoom"] = i.room
            LessonDict["lessonPrice"] = i.cost
            LessonList.append(LessonDict)
        return render_template('/other/lesson.html' , m="" , lessonList=LessonList)


@web.route("/advanced/consuming" , methods=['GET' , 'POST'])
def advancedConsuming():
    if request.method == "GET":
        return render_template('/other/consuming.html' , m="" , lessonList=[])
    else:
        betime = request.form.get("betime").split(" - ")
        start = datetime.datetime.strptime(betime[0] , "%m/%d/%Y")
        end = datetime.datetime.strptime(betime[1] , "%m/%d/%Y")
        Consumings = Consuming.query.filter(Consuming.time <= end).filter(Consuming.time >= start).all()
        ConsumingList = []
        for i in Consumings:
            ConsumingDict = {}
            ConsumingDict["customerid"] = i.customerid
            ConsumingDict["goodstype"] = "会员卡" if i.goodstype == "1" else "课程"
            ConsumingDict["time"] = i.time.strftime("%Y-%m-%d")
            ConsumingDict["goodsid"] = i.goodsid
            ConsumingList.append(ConsumingDict)
        return render_template('/other/consuming.html' , m="" , lessonList=ConsumingList)
