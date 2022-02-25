# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import extract
from watchlist.scrip import bian
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from watchlist import app, db
from watchlist.models import User, Movie, Orders, Anguser

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))
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
    if current_user.is_authenticated:
        try:
            if request.method == 'POST':
                set = int(request.args.get('set'))
                userid = current_user.id
                user = Anguser.query.filter(Anguser.userid == userid).first()
                if set == 1:
                    if user:
                        touru = request.form['touru']
                        fengxian = request.form['fengxian']
                        user.touru = touru
                        user.fengxian = fengxian
                        db.session.commit()
                        flash('机器人设置成功')
                        return redirect(url_for('edit'))
                    else:
                        flash('请先进行平台设置')
                        return redirect(url_for('settings'))
                elif set == 2:
                    zt = request.form['zt']
                    if zt == 'run':
                        user.pt_flag = 1
                    else:
                        user.pt_flag = 0
                    db.session.commit()
                    flash('更改状态成功!')
                    return redirect(url_for('edit'))
            userid = current_user.id
            user = Anguser.query.filter(Anguser.userid == userid).first()
            if user.pt_flag == 1:
                if user.pt_api_key and user.pt_secret_key:
                    run = 1
                else:
                    flash('请在设置里设置平台参数')
                    run = 0
            else:
                run = 0
            return render_template('edit.html', usertouru=user.touru, userfengxian=user.fengxian, run=run)
        except:
            return render_template('edit.html', usertouru=user.touru, userfengxian=user.fengxian, run=run)
    else:
        return render_template('index.html')

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
                    re = bian.getacc(apikey,secrekey)
                    if re:
                        user = Anguser.query.filter(Anguser.userid == userid).first()
                        if user:
                            user.pt_api_key = apikey
                            user.pt_secret_key = secrekey
                            user.pt_name = ptchance
                            user.pt_passphrase = passphrase
                            db.session.commit()
                        else:
                            wbuser = User.query.filter(User.id == userid).first()
                            user = Anguser(userid=wbuser.id, name=wbuser.name, username=wbuser.username, pt_api_key=apikey,
                                           pt_secret_key=secrekey, pt_name=ptchance, pt_passphrase=passphrase)
                            db.session.add(user)
                            db.session.commit()

                        if re['canTrade']:
                            flash('币安连接测试通过，已绑定该账户')
                            return redirect(url_for('index'))
                        else:
                            flash('币安连接测试通过，已绑定该账户，但币安平台交易权限未开通')
                            return redirect(url_for('index'))
                    else:
                        flash('币安连接测试失败，请检查平台账户')
                        return render_template('settings')
                else:
                    user = Anguser.query.filter(Anguser.userid == userid).first()
                    if user:
                        user.pt_api_key = apikey
                        user.pt_secret_key = secrekey
                        user.pt_name = ptchance
                        user.pt_passphrase = passphrase
                        db.session.commit()
                    else:
                        wbuser = User.query.filter(User.id == userid).first()
                        user = Anguser(userid=wbuser.id, name=wbuser.name, username=wbuser.username, pt_api_key=apikey,
                                       pt_secret_key=secrekey, pt_name=ptchance, pt_passphrase=passphrase)
                        db.session.add(user)
                        db.session.commit()
                    flash('Okex平台账户已绑定')
                    return redirect(url_for('index'))
            elif set == 3:
                return render_template('settings.html')
        except Exception as e:
            print('err')
    return render_template('settings.html')

@app.route('/demo',methods=['GET',"POST"])
def demo():
    try:
        userid = 3
        user = Anguser.query.filter(Anguser.userid == userid).first()
        if user:
            if user.pt_flag == 1:
                if user.pt_api_key and user.pt_secret_key:
                    run = 1
                else:
                    flash('请在设置里设置平台参数')
                    run = 0
            else:
                run = 0
        else:
            flash('请在设置里设置平台参数')
            return redirect(url_for('settings'))
            run = 0
        if request.method == 'POST':
            set = int(request.args.get('set'))
            if set == 1:
                today = datetime.now()
                info = request.form['sdate']
                info = datetime.strptime(info,'%Y-%m-%d')
                order = Orders.query.filter(extract('year', Orders.ordertime) == info.year,
                                           extract('month', Orders.ordertime) == info.month,
                                           extract('day', Orders.ordertime) == info.day,
                                            Orders.userid == userid).all()
                morder = Orders.query.filter(extract('year', Orders.ordertime) == info.year,
                                           extract('month', Orders.ordertime) == info.month,
                                           Orders.userid == userid).first()

                if order and morder:
                    order.reverse()
                    coun = round(order[0].amount,2)
                    if info.month != today.month:
                        if info.month == 12:
                            year = info.year + 1
                            month = 1
                        else:
                            year = info.year
                            month = info.month + 1
                        bmorder = Orders.query.filter(extract('year', Orders.ordertime) == year,
                                                      extract('month', Orders.ordertime) == month,
                                                      Orders.userid == userid).first()

                        if bmorder:
                            mfig = round((bmorder.amount - morder.amount), 2)
                        else:
                            mfig = 0
                    else:
                        mfig = round((order[0].amount - morder.amount), 2)
                    figsum = 0
                    for a in order:
                        figsum = a.fig + figsum
                    return render_template('orders.html', info=order, coun=coun, figsum=figsum, run=run, mfig=mfig)
                else:
                    return render_template('orders.html', info=None, coun=None, figsum=0, run=run, mfig=0)
            elif set == 2:
                zt = request.form['zt']
                if zt == 'run':
                    user.pt_flag = 1
                else:
                    user.pt_flag = 0
                db.session.commit()
                flash('更改状态成功!')
                return redirect(url_for('demo'))
        else:
            today = datetime.now()
            userid = 3
            if userid:
                order = Orders.query.filter(extract('year', Orders.ordertime) == today.year,
                                           extract('month', Orders.ordertime) == today.month,
                                           extract('day', Orders.ordertime) == today.day,
                                        Orders.userid == userid).all()
                morder = Orders.query.filter(extract('year', Orders.ordertime) == today.year,
                                             extract('month', Orders.ordertime) == today.month,
                                             Orders.userid == userid).first()
                if order and morder:
                    order.reverse()
                    coun = round(order[0].amount, 2)
                    mfig = round((coun - morder.amount), 2)
                    figsum = 0
                    for a in order:
                        figsum = a.fig + figsum
                    return render_template('demo.html', info=order, coun=coun, figsum=figsum, run=run, mfig=mfig)
                else:
                    return render_template('demo.html', info=None, coun=None, figsum=0, run=run, mfig=0)
            else:
                return redirect(url_for('login'))

    except Exception as e:
        flash('获取失败，请刷新页面重试')
        return render_template('demo.html', info=None, coun=None, figsum=0, run=0)

@app.route('/orders',methods=['GET',"POST"])
@login_required
def orders():
    try:
        userid = current_user.id
        user = Anguser.query.filter(Anguser.userid == userid).first()
        if user:
            name = user.name
            if user.pt_flag == 1:
                if user.pt_api_key and user.pt_secret_key:
                    run = 1
                else:
                    flash('请在设置里设置平台参数')
                    run = 0
            else:
                run = 0
        else:
            flash('请在设置里设置平台参数')
            return redirect(url_for('settings'))
            run = 0
        if request.method == 'POST':
            set = int(request.args.get('set'))
            if set == 1:
                today = datetime.now()
                info = request.form['sdate']
                info = datetime.strptime(info,'%Y-%m-%d')
                order = Orders.query.filter(extract('year', Orders.ordertime) == info.year,
                                           extract('month', Orders.ordertime) == info.month,
                                           extract('day', Orders.ordertime) == info.day,
                                            Orders.userid == userid).all()
                morder = Orders.query.filter(extract('year', Orders.ordertime) == info.year,
                                           extract('month', Orders.ordertime) == info.month,
                                           Orders.userid == userid).first()

                if order and morder:
                    order.reverse()
                    coun = round(order[0].amount,2)
                    if info.month != today.month:
                        if info.month == 12:
                            year = info.year + 1
                            month = 1
                        else:
                            year = info.year
                            month = info.month + 1
                        bmorder = Orders.query.filter(extract('year', Orders.ordertime) == year,
                                                      extract('month', Orders.ordertime) == month,
                                                      Orders.userid == userid).first()

                        if bmorder:
                            mfig = round((bmorder.amount - morder.amount), 2)
                        else:
                            mfig = 0
                    else:
                        mfig = round((order[0].amount - morder.amount), 2)
                    figsum = 0
                    for a in order:
                        figsum = a.fig + figsum
                    return render_template('orders.html',name=name, info=order, coun=coun, figsum=figsum, run=run, mfig=mfig)
                else:
                    return render_template('orders.html',name=name, info=None, coun=None, figsum=0, run=run, mfig=0)
            elif set == 2:
                zt = request.form['zt']
                if zt == 'run':
                    user.pt_flag = 1
                else:
                    user.pt_flag = 0
                db.session.commit()
                flash('更改状态成功!')
                return redirect(url_for('orders'))
        else:
            today = datetime.now()
            userid = current_user.id
            if userid:
                order = Orders.query.filter(extract('year', Orders.ordertime) == today.year,
                                           extract('month', Orders.ordertime) == today.month,
                                           extract('day', Orders.ordertime) == today.day,
                                        Orders.userid == userid).all()
                morder = Orders.query.filter(extract('year', Orders.ordertime) == today.year,
                                             extract('month', Orders.ordertime) == today.month,
                                             Orders.userid == userid).first()
                if order and morder:
                    order.reverse()
                    coun = round(order[0].amount, 2)
                    mfig = round((coun - morder.amount), 2)
                    figsum = 0
                    for a in order:
                        figsum = a.fig + figsum
                    return render_template('orders.html', name=name, info=order, coun=coun, figsum=figsum, run=run, mfig=mfig)
                else:
                    return render_template('orders.html', name=name, info=None, coun=None, figsum=0, run=run, mfig=0)
            else:
                return redirect(url_for('login'))

    except Exception as e:
        flash('获取失败，请刷新页面重试')
        return render_template('orders.html', info=None, coun=None, figsum=0, run=0)

@app.route('/public', methods=['GET', 'POST'])
def public():
    return render_template('public.html')
@app.route('/usermanage', methods=['GET', 'POST'])
@login_required
def usermanage():
    if current_user.admin == 1:
        webuser = User.query.filter().all()
    else:
        webuser = User.query.filter(User.recom == current_user.id)
        if not webuser:
            webuser = []
        else:
            userid = webuser[0].id
    if request.method == 'POST':
        flag = request.args.get('flag')
        if flag == '1':
            userid = request.form['userid']
            today = datetime.now()
            order = Orders.query.filter(extract('year', Orders.ordertime) == today.year,
                                        extract('month', Orders.ordertime) == today.month,
                                        extract('day', Orders.ordertime) == today.day,
                                        Orders.userid == userid).all()
            if order:
                order.reverse()
                order = order[0]
                order.name = User.query.filter(User.id == userid).first().name
                return render_template('usermanage.html', webuser=webuser, order=order)
            else:
                return render_template('usermanage.html', webuser=webuser, order=None, userid=userid)
        elif flag == '2':
            userid = request.form['userid']
            if userid == current_user.id:
                flash('不能删除自己')
                return redirect(url_for('usermanage'))
            else:
                user = User.query.filter(User.id == userid).first()
                db.session.delete(user)
                anguser = Anguser.query.filter(Anguser.userid == userid).first()
                if anguser:
                    db.session.delete(anguser)
                    db.session.commit()
                else:
                    db.session.commit()
                flash('删除成功!')
                return redirect(url_for('usermanage'))

        elif flag == '3':
            recom = current_user.id
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            wbuser = User(username=username, name=name, recom=recom)
            wbuser.set_password(password)
            db.session.add(wbuser)
            db.session.commit()
            adduser = User.query.filter(User.username == username)
            if adduser:
                flash('新增成功')
                return redirect(url_for('usermanage'))
            else:
                flash('新增失败,稍后再试!')
                return redirect(url_for('usermanage'))

    today = datetime.now()
    order = Orders.query.filter(extract('year', Orders.ordertime) == today.year,
                                extract('month', Orders.ordertime) == today.month,
                                extract('day', Orders.ordertime) == today.day,
                                Orders.userid == userid).all()
    if order:
        order.reverse()
        order = order[0]
        order.name = User.query.filter(User.id == userid).first().name
        return render_template('usermanage.html', webuser=webuser, order=order)
    else:
        return render_template('usermanage.html', webuser=webuser, order=None, userid=userid)



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
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        try:
            if username == user.username and user.validate_password(password):
                if user.admin == 1 or user.admin == 2:
                    login_user(user, remember=remember, admin=True)

                    return redirect(url_for('index'))
                else:
                    login_user(user, remember=remember)

                    return redirect(url_for('index'))
            else:
                flash('用户名或密码不正确')
                return redirect(url_for('login'))
        except:
            flash('用户名或密码不正确')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('testt.html')
