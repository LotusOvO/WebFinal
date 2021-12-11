import os

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import *
from goods import *
from mail import *
from database import *
from users import *
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.debug = True
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
bootstrap = Bootstrap(app=app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message = '请先登录'
login_manager.init_app(app=app)


@login_manager.user_loader
def load_user(username):
    return User.get(username)


@app.route('/', methods=['POST', 'GET'])
def hello():
    return redirect(url_for('home'))


@app.route('/home', methods=["POST", "GET"])
def home():
    ls = showgood()
    return render_template("index.html", form=ls)


@app.route('/register', methods=['POST', 'GET'])
def register():
    registerfrom = RegisterForm()
    if request.method == "POST":
        username = registerfrom.username.data
        password = registerfrom.pwd.data
        repassword = registerfrom.re_pwd.data
        if finduser(username):
            flash("用户名已存在")
            return redirect(url_for('register'))

        if password != repassword:
            flash("两次密码不一致")
            return redirect(url_for('register'))

        newuser(username, password)
        return redirect(url_for('login'))
    return render_template("register.html", form=registerfrom)


@app.route('/login', methods=['POST', 'GET'])
def login():
    loginfrom = LoginForm()
    if request.method == "POST":
        username = loginfrom.username.data
        password = loginfrom.pwd.data
        user = User(username)
        if userlogin(username, password):
            session['user_shopping_trolley'] = []
            login_user(user)
            if username == 'admin':
                flash("管理员用户")
                return redirect(url_for('manage'))
            flash("欢迎" + username)
            return redirect(url_for('home'))
        else:
            flash("用户名或密码错误")
            return redirect(url_for('login'))
    return render_template("login.html", form=loginfrom)


@app.route('/shoppingtrolley', methods=['POST', 'GET'])
@login_required
def shoppingtrolley():
    ls = []
    for item in session.get("user_shopping_trolley"):
        goodform = GoodForm()
        goodform.ID.data = item[0]
        goodform.name.data = item[1]
        goodform.price.data = item[2]
        goodform.number.data = item[3]
        ls.append(goodform)
    return render_template("shoppingtrolley.html", form=ls)


@app.route('/payment', methods=['POST', 'GET'])
@login_required
def payment():
    emailform = EmailForm()
    if request.method == "POST":
        context = ""
        gooddict = {}
        for item in session.get("user_shopping_trolley"):
            if item[0] in gooddict:
                gooddict[item[0]][0] += 1
            else:
                gooddict[item[0]] = [1, item[1], item[2]]
        for key in gooddict:
            good = findbyid(key)
            if good['inventory'] < gooddict[key][0]:
                flash(good['name'] + "库存不足")
                return redirect(url_for('shoppingtrolley'))
        for key in gooddict:
            good = gooddict[key]
            context += f"商品：{good[1]}    售价：￥{good[2]}    数量：{good[0]}\n"
            salegood(key, good[0])
            addorder(current_user.username, good[1], good[2], good[0])
        Sendmail(context, emailform.email.data)
        flash("购买成功")
        res = session.get('user_shopping_trolley')
        res.clear()
        session['user_shopping_trolley'] = res
        return redirect(url_for('home'))
    return render_template("payment.html", form=emailform)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    session["user_shopping_trolley"].clear()
    return redirect(url_for('home'))


@app.route('/addshoppingtrolley/<id>', methods=['POST', 'GET'])
@login_required
def addshoppingtrolley(id):
    res = session.get("user_shopping_trolley")
    res.append(findbyid(id))
    session["user_shopping_trolley"] = res
    return redirect(url_for('home'))


@app.route('/removeshoppingtrolley/<id>', methods=['POST', 'GET'])
@login_required
def removeshoppingtrolley(id):
    res = session.get("user_shopping_trolley")
    for item in res:
        if item[0] == int(id):
            res.remove(item)
            session["user_shopping_trolley"] = res
            break
    return redirect(url_for('shoppingtrolley'))


@app.route('/manage', methods=["POST", "GET"])
@login_required
def manage():
    ls = showgood()
    newgoodform = GoodForm()
    if request.method == "POST" and newgoodform.validate_on_submit():
        name = newgoodform.name.data
        price = newgoodform.price.data
        num = newgoodform.number.data
        addgood(name, num, price)
        return redirect(url_for('manage'))
    return render_template("manage.html", form=ls, newgood=newgoodform)


@app.route('/removegood/<id>', methods=["POST", "GET"])
def removegood(id):
    delgood(id)
    return redirect(url_for('manage'))


@app.route('/changegood/<id>', methods=["POST", "GET"])
def modifigood(id):
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        num = request.form['num']
        changegood(id, name, price, num)
    return redirect(url_for('manage'))


@app.route('/orders/<username>', methods=["POST", "GET"])
@login_required
def orders(username):
    order = []
    if username == 'admin':
        order = gerallorder()
    else:
        order = getorderbyuser(username)
    return render_template("orders.html", order=order)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
