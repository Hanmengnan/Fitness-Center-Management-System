import datetime

from flask import url_for , redirect , render_template , request
from flask_admin import helpers as admin_helpers
from flask_security import current_user
from flask_security import login_required , login_user , logout_user

from apps import admin
from . import web


def getc():
    cnum = len(Customer.query.filter_by().all())
    coaches = Coach.query.filter_by().all()
    coachList = []

    for i in coaches:
        t = 0
        for j in i.lessons:
            t += len(j.customers.all())
        cdict = {"name": i.name , "popular": int(100 * t / cnum) , "num": len(i.lessons)}
        coachList.append(cdict)
    return coachList


def getl():
    cnum = len(Customer.query.filter_by().all())
    lessons = Lesson.query.filter_by().all()
    lessonList = []
    for i in lessons:
        ldict = {"name": i.lessonName , "num": len(i.customers.all()) ,
                 "popular": int(100 * len(i.customers.all()) / cnum)}
        lessonList.append(ldict)
    return lessonList


@web.context_processor
def web_context_processor():
    return dict(
        admin_base_template=admin.base_template ,
        admin_view=admin.index_view ,
        get_url=url_for ,
        h=admin_helpers ,
    )


@web.route("/")
def init():
    return redirect(url_for('web.index'))


@web.route("/admin")
def index():
    return render_template('admin/mybase.html')


from apps.web.forms import *
from apps import user_datastore
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
        customerID = form.customerid.data
        password = form.password.data
        re_password = form.re_password.data
        if password != re_password:
            return render_template('login/register.html' , form=form , m="两次输入密码不一致")

        if Customer.query.filter_by(id=customerID).first() == None:
            return render_template('login/register.html' , form=form , m="会员号码不存在，请联系管理员")

        if User.query.filter_by(name=username).first() != None:
            return render_template('login/register.html' , form=form , m="该用户名已存在")

        role = user_datastore.find_role("user")
        user = user_datastore.create_user(name=username , email=email , password=password , customerID=customerID)
        user_datastore.add_role_to_user(user , role)

        a = Authority(
            userId=customerID ,
            customerDetail=False ,
            customerManage=False ,
            lessonDetail=False ,
            lessonManage=False ,
            coachDetail=False ,
            coachManage=False ,
            cardDetail=False ,
            cardManage=False ,
            leaveManage=False ,
            userAdd=False ,
            userEdit=False ,
            userDelete=False
        )
        db.session.add(a)
        db.session.commit()
        return redirect('/login')

    return render_template('login/register.html' , form=form , m="")


def notify():
    id = current_user.customerID
    t = datetime.datetime.now()

    leave = count = overdue = 0

    l = Leave.query.filter_by(customerid=id).first()
    if l != None and t < l.endtime:
        leave = 1

    cards = VipCard.query.filter_by(customer=id)
    for c in cards:
        print(c.overdue_Date)
        if c.overdue_Date < t:
            count += 1
            overdue = 1
    return leave , overdue , count


@web.route("/profile" , methods=['GET'])
def profile():
    from apps.model import Customer
    customerID = current_user.customerID
    customer = Customer.query.filter_by(id=customerID).first()
    name = customer.name
    sex = customer.sex
    hcondition = customer.hcondition
    address = customer.adress
    sid = customer.sid
    phoneNumber = customer.phoneNumber
    money = customer.money
    leavef , overdue , count = notify()

    return render_template('other/index.html' , **locals() , m="")


@web.route("/profile/<action>" , methods=['POST' , "GET"])
def profileAction(action):
    if request.method == "GET":
        return redirect("/profile")

    from flask_security import current_user

    customerID = current_user.customerID
    customer = Customer.query.filter_by(id=customerID).first()
    name = customer.name
    sex = customer.sex
    hcondition = customer.hcondition
    address = customer.adress
    sid = customer.sid
    phoneNumber = customer.phoneNumber
    money = customer.money

    leavef , overdue , count = notify()

    if action == "transferCard":
        cid = request.form.get("cardid")
        uid = request.form.get("userid")
        old_owner = VipCard.query.filter_by(customer=customerID , id=cid).first()
        aim_customer = Customer.query.filter_by(id=uid).first()
        if aim_customer and old_owner:
            VipCard.query.filter_by(customer=customerID , id=cid).update({"customer": int(uid)})
            db.session.commit()
            return render_template('other/index.html' , **locals() , m="操作成功")
        else:
            return render_template('other/index.html' , **locals() , m="操作失败")

    elif action == "leave":
        dayNum = request.form.get("dayNum")

        leave = Leave.query.filter_by(customerid=customerID).first()
        if leave == None:
            nowTime = datetime.datetime.now()
            endTime = nowTime + datetime.timedelta(days=int(dayNum))
            newLeave = Leave(customerID , nowTime , endTime)
            db.session.add(newLeave)
        else:
            leave.endtime = leave.endtime + datetime.timedelta(days=int(dayNum))

        vipcards = VipCard.query.filter_by(customer=customerID)
        for card in vipcards:
            date = card.overdue_Date + datetime.timedelta(days=int(dayNum))
            VipCard.query.filter_by(id=card.id).update({"overdue_Date": date})

        db.session.commit()
        return redirect('/profile')

    elif action == "buyCard":
        cardid = request.form.get("cardid")
        card = VipCard.query.filter_by(id=cardid).first()
        if card != None:
            if customer.money >= card.price:
                if card.saled == True:
                    if card.customer == customerID:
                        date = card.overdue_Date + datetime.timedelta(days=365)
                        VipCard.query.filter_by(id=card.id).update({"overdue_Date": date})
                        Customer.query.filter_by(id=customerID).update({"money": customer.money - card.price})
                        db.session.commit()
                        # return render_template('other/index.html' , **locals() , m="操作成功")
                        return redirect('/profile')
                    else:
                        return render_template('other/index.html' , **locals() , m="该卡为别人所有，不能购买")
                else:
                    VipCard.query.filter_by(id=card.id).update({"customer": customerID , "saled": True})
                    Customer.query.filter_by(id=customerID).update({"money": customer.money - card.price})
                    db.session.add(Consuming(customerid=customerID , goodstype="会员卡" , goodsid=cardid ,
                                             time=datetime.datetime.now()))
                    db.session.commit()
                    # return render_template('other/index.html' , **locals() , m="操作成功")
                    return redirect('/profile')
            else:
                return render_template('other/index.html' , **locals() , m="金额不足")
        else:
            return render_template('other/index.html' , **locals() , m="卡号错误")

    elif action == "buyLesson":
        cardid = request.form.get("cardid")
        lessonid = request.form.get("lessonid")

        customer = Customer.query.filter_by(id=customerID).first()
        if cardid == "":
            card = None
            discount = 1
        else:
            card = VipCard.query.filter_by(id=cardid).first()
            discount = card.discount

        lesson = Lesson.query.filter_by(id=lessonid).first()
        leave = Leave.query.filter_by(customerid=customerID).first()
        if leave != None:
            if datetime.datetime.now() > leave.endtime:
                leave = Leave.query.filter_by(customerid=customerID).delete()
            else:
                return render_template('other/index.html' , **locals() , m="请假期间不能消费 ")

        if card != None and card.customer != customerID:
            return render_template('other/index.html' , **locals() , m="卡号错误")
        elif lesson == None:
            return render_template('other/index.html' , **locals() , m="课程号错误")
        elif lesson in customer.lessons:
            return render_template('other/index.html' , **locals() , m="课程已购买")
        else:
            r = (customer.money) - (lesson.cost * discount)
            if r < 0:
                return render_template('other/index.html' , **locals() , m="金额不足")
            else:
                c = Customer.query.filter_by(id=customerID)
                c.update({"money": r})
                c.first().lessons.append(lesson)
                db.session.add(
                    Consuming(customerid=customerID , goodstype="课程" , goodsid=lessonid , time=datetime.datetime.now()))
                db.session.commit()
                return redirect('/profile')
    else:
        return render_template('other/index.html' , **locals() , m="非法操作")


@web.route("/advanced/lesson" , methods=['GET' , 'POST'])
def advancedLesson():
    if request.method == "GET":
        return render_template('/other/lesson.html' , ls=getl() , cs=getc() , m="" , lessonList=[])
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
        return render_template('/other/lesson.html' , ls=getl() , cs=getc() , m="" , lessonList=LessonList)


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
            ConsumingDict["goodstype"] = i.goodstype
            ConsumingDict["time"] = i.time.strftime("%Y-%m-%d")
            ConsumingDict["goodsid"] = i.goodsid
            ConsumingList.append(ConsumingDict)
        return render_template('/other/consuming.html' , m="" , lessonList=ConsumingList)


@web.route("/authority" , methods=['POST' , 'GET'])
def authority():
    form = authorityForm()
    print(form.query.data)
    if form.validate_on_submit():
        roleName = form.roleName.data
        query = form.query.data
        modify = form.modify.data
        if query == True:
            a = Authority.query.filter_by(roleName=roleName).first()
            form.c1.data = a.customerDetail
            form.c2.data = a.customerManage
            form.c3.data = a.lessonDetail
            form.c4.data = a.lessonManage
            form.c5.data = a.coachDetail
            form.c6.data = a.coachManage
            form.c7.data = a.cardDetail
            form.c8.data = a.cardManage
            form.c9.data = a.leaveManage
            form.c10.data = a.userAdd
            form.c11.data = a.userEdit
            form.c12.data = a.userDelete
        else:

            c1 = form.c1.data
            c2 = form.c2.data
            c3 = form.c3.data
            c4 = form.c4.data
            c5 = form.c5.data
            c6 = form.c6.data
            c7 = form.c7.data
            c8 = form.c8.data
            c9 = form.c9.data
            c10 = form.c10.data
            c11 = form.c11.data
            c12 = form.c12.data

            Authority.query.filter_by(roleName=roleName).update({
                "customerDetail": c1 ,
                "customerManage": c2 ,
                "lessonDetail": c3 ,
                "lessonManage": c4 ,
                "coachDetail": c5 ,
                "coachManage": c6 ,
                "cardDetail": c7 ,
                "cardManage": c8 ,
                "leaveManage": c9 ,
                "userAdd": c10 ,
                "userEdit": c11 ,
                "userDelete": c12
            })
            db.session.commit()

    return render_template('/other/authoityManage.html' , form=form)
