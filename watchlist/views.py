# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import extract
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

    movies = Movie.query.all()
    # testuser = User.get_id()
    # print('testuser=', testuser)
    return render_template('index.html', movies=movies)
@app.route('/binan',methods=['GET','POST'])
def binan():
    # if request.method == 'POST':
    #     info = request.values.to_dict()
    #     r, s = binance.getstick(limit=10, starttime=info['opentime'], symbol=info['symbol'])
    #     return render_template('binan.html', mticks=r, symbol=s)
    #
    # r, s = binance.getstick(limit=10)
    # r.reverse()

    #return render_template('binan.html', mticks=r, symbol=s)
    return render_template('binan.html')

@app.route('/playvideo/<movie_name>', methods = ['GET','POST'])
@login_required
def play(movie_name):
    return render_template('playvideo.html',movie_name=movie_name)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        filename = request.form['filename']
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        movie.filename = filename
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


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
                user = Anguser.query.filter(Anguser.userid == userid).first()
                if user:
                    user.pt_api_key = apikey
                    user.pt_secret_key = secrekey
                    user.pt_name = ptchance
                    user.pt_passphrase = passphrase
                    db.session.commit()
                    flash('平台设置成功')
                    return redirect(url_for('index'))
                else:
                    wbuser = User.query.filter(User.id == userid).first()
                    user = Anguser(userid=wbuser.id, name=wbuser.name, username=wbuser.username, pt_api_key=apikey,
                                   pt_secret_key=secrekey, pt_name=ptchance, pt_passphrase=passphrase)
                    db.session.add(user)
                    db.session.commit()
                    flash('平台设置成功')
                    return render_template('usermanageusermanage.html', a=user, b='touru')
            elif set == 3:
                user = Anguser.query.filter(Anguser.userid == userid).first()
                if user:
                    touru = request.form['touru']
                    fengxian = request.form['fengxian']
                    user.touru = touru
                    user.fengxian = fengxian
                    db.session.commit()
                    flash('机器人设置成功')
                    return redirect(url_for('index'))
                else:
                    flash('请先进行平台设置')
                    return render_template('usermanageusermanage.html', a=user, b='touru')
        except Exception as e:
            print('err')
    return render_template('settings.html')

@app.route('/orders',methods=['GET',"POST"])
@login_required
def orders():
    try:
        userid = current_user.id
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
                info = request.form['sdate']
                info = datetime.strptime(info,'%Y-%m-%d')
                order = Orders.query.filter(extract('year', Orders.ordertime) == info.year,
                                           extract('month', Orders.ordertime) == info.month,
                                           extract('day', Orders.ordertime) == info.day,
                                            Orders.userid == userid).all()
                if order:
                    order.reverse()
                    coun = round((order[0].amount - order[0].acc_wsx),2)
                    figsum = 0
                    for a in order:
                        figsum = a.fig + figsum
                    return render_template('orders.html', info=order, coun=coun, figsum=figsum, run=run)
                else:
                    return render_template('orders.html', info=None, coun=None, figsum=0, run=run)
            elif set == 2:
                zt = request.form['zt']
                if zt == 'run':
                    user.pt_flag = 1
                else:
                    user.pt_flag = 0
                db.session.commit()
                flash('更改状态成功!')
                return redirect(url_for('orders'))
        today = datetime.now()
        userid = current_user.id
        if userid:
            order = Orders.query.filter(extract('year', Orders.ordertime) == today.year,
                                       extract('month', Orders.ordertime) == today.month,
                                       extract('day', Orders.ordertime) == today.day,
                                    Orders.userid == userid).all()
            if order:
                order.reverse()
                coun = round((order[0].amount - order[0].acc_wsx),2)
                figsum = 0
                for a in order:
                    figsum = a.fig + figsum
                return render_template('orders.html', info=order, coun=coun, figsum=figsum, run=run)
            else:
                return render_template('orders.html', info=None, coun=None, figsum=0, run=run)
        else:
            return redirect(url_for('login'))

    except Exception as e:
        flash('获取失败，请刷新页面重试')
        return render_template('orders.html', info=None, coun=None, figsum=0, run=0)
@app.route('/usermanage', methods=['GET', 'POST'])
def usermanage():
    if current_user.admin == 1:
        webuser = User.query.filter().all()
    else:
        webuser = User.query.filter(User.recom == current_user.id)
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
    userid = current_user.id
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
                if user.admin == 1:
                    login_user(user, remember=remember, admin=True)
                    flash('登录成功')
                    return redirect(url_for('orders'))
                else:
                    login_user(user, remember=remember)
                    flash('登录成功')
                    return redirect(url_for('orders'))
            else:
                flash('用户名或密码不正确')
                return redirect(url_for('login'))
        except:
            flash('网络故障')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

