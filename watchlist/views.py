# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import extract
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from watchlist.scrip import binance #command
from watchlist import app, db
from watchlist.models import User, Movie, Orders

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
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')

@app.route('/orders',methods=['GET',"POST"])
@login_required
def orders():
    try:
        if request.method == 'POST':
            if current_user.is_authenticated:
                userid = current_user.id
                info = request.form['sdate']
                info = datetime.strptime(info,'%Y-%m-%d')
                order = Orders.query.filter(extract('year', Orders.ordertime) == info.year,
                                           extract('month', Orders.ordertime) == info.month,
                                           extract('day', Orders.ordertime) == info.day,
                                            Orders.userid == userid).all()
                if order:
                    order.reverse()
                    coun = len(order)
                    figsum = 0
                    for o in order:
                        figsum = figsum + o.fig
                    figsum = round(figsum,2)
                    return render_template('orders.html', info=order, coun=coun, figsum=figsum)
            else:
                return render_template('orders.html', info=None, coun=None, figsum=None)
        today = datetime.now()
        userid = current_user.id
        if userid:
            order = Orders.query.filter(extract('year', Orders.ordertime) == today.year,
                                       extract('month', Orders.ordertime) == today.month,
                                       extract('day', Orders.ordertime) == today.day,
                                    Orders.userid == userid).all()
            if order:
                order.reverse()
                coun = len(order)
                figsum = 0
                for o in order:
                    figsum = figsum + o.fig
                figsum = round(figsum, 2)
                return render_template('orders.html', info=order, coun=coun, figsum=figsum)
            else:
                return render_template('orders.html', info=None, coun=None, figsum=None)
        else:
            return redirect(url_for('login'))

    except:
        flash('获取失败，请刷新页面重试')
        return render_template('orders.html', info=None, coun=None, figsum=None)
@app.route('/test', methods=['GET', 'POST'])
def test():
    #a = User.get_id(user)

    a = current_user
    if a.is_anonymous:
        a = '游客'

    else:
        a = a.id
    return render_template('test.html', a=a)
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
                login_user(user, remember=remember)
                flash('登录成功')
                return redirect(url_for('orders'))
        except:
            flash('用户名或密码不正确')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))
