# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import extract
from watchlist import app, db
from watchlist.models import User, Movie
from watchlist.scrip import bian, command


@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        logined = 1
        role = current_user.admin
    else:
        logined = 0
        role = 0
    king = ['ETH', 'BTC', 'DOGE']
    info = []
    for i in king:
        x = bian.getprice(i)
        if x:
            x["priceChangePercent"] = float(x["priceChangePercent"])
            x['symbol'] = x['symbol'].split('USD')[0]
            info.append(x)
    if not info:
        info = False
    return render_template('index.html', info=info)
@app.route('/explain',methods=['GET', 'POST'])
def explain():
    # if current_user.is_authenticated:
    #     return render_template('binan.html')
    #
    # return redirect(url_for('login'))
    return render_template('explain.html')
@app.route('/binan',methods=['GET', 'POST'])
def binan():
    # if current_user.is_authenticated:
    #     return render_template('binan.html')
    #
    # return redirect(url_for('login'))
    return render_template('binan.html')
@app.route('/okex',methods=['GET', 'POST'])
def okex():
    # if current_user.is_authenticated:
    #     return render_template('binan.html')
    #
    # return redirect(url_for('login'))
    return render_template('okex.html')
@app.route('/subacc', methods = ['GET','POST'])
def subacc():
    return render_template('subacc.html')

@app.route('/movie/edit', methods=['GET', 'POST'])
@login_required
def edit():
    userid = current_user.id
    user = command.getuser(userid)
    if user[0]:
        user = user[1]
    else:
        flash('网络故障，稍后再试')
        return render_template('index.html')
    try:
        if request.method == 'POST':
            set = int(request.args.get('set'))
            if set == 1:
                setrun = command.setrun(userid)
                if setrun[0]:
                    flash('机器人设置成功')
                    return redirect(url_for('edit'))
                else:
                    if setrun[1] == 'nokey':
                        flash('未绑定平台账户，请先绑定')
                        return redirect(url_for('settings'))
                    flash('未设置成功，稍后再试')
                    return redirect(url_for('settings'))
            elif set == 2:
                lever = request.form['lever']
                fengxian = request.form['fengxian']
                re = command.rootset(userid,lever,fengxian)
                if re[0]:
                    flash('设置成功')
                else:
                    flash('网络故障，设置失败')
                return redirect(url_for('settings'))
        if user['pt_flag'] == 1:
                run = 1
        else:
                run = 0
        return render_template('edit.html', userlever=user['touru'], userfengxian=user['fengxian'], run=run)
    except:
        return render_template('edit.html', userlever=user['touru'], userfengxian=user['fengxian'], run=run)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        try:
            userid = current_user.id
            set = int(request.args.get('set'))
            if set == 1:
                name = request.form['name']
                if not name or len(name) > 20:
                    flash('名字不能大于10')
                    return redirect(url_for('settings'))
                password = request.form['password']
                if not password or len(password) < 6 or len(password) > 20:
                    flash('密码需要大于6')
                    return redirect(url_for('settings'))
                wbuser = User.query.filter(User.id == userid).first()
                wbuser.username = name
                wbuser.set_password(password)
                db.session.commit()
                flash('修改成功,请重新登录')
                logout_user()
                return redirect(url_for('index'))
            elif set == 2:
                apikey = request.form['apikey']
                ptchance = request.form['ptchance']
                secrekey = request.form['secrekey']
                passphrase = request.form['passphrase']
                if ptchance == 'bianace':
                    testre = bian.getacc(apikey,secrekey)
                    if testre:
                        if testre['canTrade']:
                            re = command.setapikey(userid, key=apikey, secrekey=secrekey)
                            if re[0]:
                                flash('币安连接测试通过，已绑定该账户')
                                return render_template('settings.html')
                            else:
                                flash(re[1])
                                return render_template('settings.html')
                        else:
                            flash('币安连接测试通过，但币安平台交易权限未开通，请开通后绑定')
                            return render_template('settings.html')
                    else:
                        flash('币安连接测试失败，请检查平台账户')
                        return render_template('settings')
            elif set == 3:
                return render_template('settings.html')
        except Exception as e:
            print(e)
    return render_template('settings.html')

@app.route('/demo',methods=['GET',"POST"])
def demo():
    userid = 5
    try:
        today = datetime.now()
        if request.method == 'POST':
            info = request.form['sdate']
            info = datetime.strptime(info, '%Y-%m-%d')
        else:
            info = today
        getorders = command.getorder(userid, year=info.year, month=info.month, day=info.day)
        if getorders[0]:
            orders = getorders[1]
            orders.reverse()
            coun = round(orders[0]['amount'], 2)
            dfig = 0
            for t in orders:
                dfig = dfig + t['fig']
        else:
            coun = 0
            dfig = 0
            orders = None
        figs = command.gettotalfig(userid, year=info.year, month=info.month)
        mfig = 0
        if figs:
            for t in figs[1]:
                mfig = mfig + t
        return render_template('demo.html', info=orders, coun=coun, figsum=dfig, mfig=mfig, month=info.month)
    except Exception as e:
        flash('获取失败，请刷新页面重试')
        return render_template('demo.html', info=None, coun=None, figsum=0, run=0)

@app.route('/orders',methods=['GET',"POST"])
@login_required
def orders():
    userid = current_user.id
    try:
        today = datetime.now()
        if request.method == 'POST':
            info = request.form['sdate']
            info = datetime.strptime(info, '%Y-%m-%d')
        else:
            info = today
        getorders = command.getorder(userid, year=info.year, month=info.month, day=info.day)
        if getorders[0]:
            orders = getorders[1]
            orders.reverse()
            coun = round(orders[0]['amount'], 2)
            dfig = 0
            for t in orders:
                dfig = dfig + t['fig']
        else:
            coun = 0
            dfig = 0
            orders = None
        figs = command.gettotalfig(userid, year=info.year, month=info.month)
        mfig = 0
        if figs:
            for t in figs[1]:
                mfig = mfig + t
        return render_template('orders.html', info=orders, coun=coun, figsum=dfig, mfig=mfig, month=info.month)
    except Exception as e:
        flash('获取失败，请刷新页面重试')
        return render_template('orders.html', info=None, coun=None, figsum=0, run=0)

@app.route('/public', methods=['GET', 'POST'])
def public():
    return render_template('public.html')
@app.route('/usermanage', methods=['GET', 'POST'])
@login_required
def usermanage():
    if current_user.id == 1:
        webuser = User.query.filter().all()
    else:
        webuser = User.query.filter(User.recom == current_user.id).all()
    if request.method == 'POST':
        flag = request.args.get('flag')
        if flag == '1':
            userid = request.form['userid']
            userstatu = command.getuserstatu(userid)
            if userstatu[0]:
                order = userstatu[1]
                return render_template('usermanage.html', webuser=webuser, order=order)
            else:
                return render_template('usermanage.html', webuser=webuser, order=None, userid=userid)
        elif flag == '2':
            userid = request.form['userid']
            if userid == current_user.id:
                flash('不能删除自己')
                return redirect(url_for('usermanage'))
            else:
                delauto = command.deluser(current_user.id, userid)
                if delauto:
                    user = User.query.filter(User.id == userid).first()
                    db.session.delete(user)
                    flash('删除成功!')
                    return redirect(url_for('usermanage'))
                else:
                    flash('网络故障，稍后再试！')
                    return redirect(url_for('usermanage'))
        elif flag == '3':
            recom = current_user.id
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            wbuser = User(username=username, name=name, recom=recom)
            if db.Query(User).filter_by(username=username):
                flash('登录名不可用，请重新输入')
                return redirect(url_for('usermanage'))
            if db.Query(User).filter_by(name=name):
                flash('用户名不可用，请重新输入')
                return redirect(url_for('usermanage'))
            wbuser.set_password(password)
            db.session.add(wbuser)
            db.session.commit()
            adduser = User.query.filter(User.username == username)
            if adduser:
                command.adduser(current_user.id, adduser)
                flash('新增成功')
                return redirect(url_for('usermanage'))
            else:
                flash('新增失败,稍后再试!')
                return redirect(url_for('usermanage'))
    return render_template('usermanage.html', webuser=webuser, order=None)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.args.get('remenber')
        if remember:
            remember = True
        else:
            remember = False
        if not username or not password:
            flash('无效的 username 或 password.')
            return render_template('login.html')

        user = User.query.filter_by(username=username).first()
        if user:
            if username == user.username and user.validate_password(password):
                login_user(user, remember=remember)
                flash('登录成功！')
                return redirect(url_for('index'))
            else:
                flash('密码不正确')
                return render_template('login.html')
        else:
            flash('登录名不正确')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('testt.html')
