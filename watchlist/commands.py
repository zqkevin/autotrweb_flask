# -*- coding: utf-8 -*-
import click
from datetime import datetime
from watchlist import app, db, models
from watchlist.models import User, Movie
from watchlist.scrip import bian,command



@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    db.drop_all()
    """Generate fake data."""
    db.create_all()

    name = 'Kevin P'
    user = User(name=name)
    db.session.add(user)
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988', 'filename': 'video.mp4'},
        {'title': 'Dead Poets Society', 'year': '1989','filename': '631.mp4'},
        {'title': 'A Perfect World', 'year': '1993','filename': 'video.mp4'},
    ]
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'], filename=m['filename'])
        db.session.add(movie)
    res = bian.getstick()[0]
    for r in res:
        eth = Ethusdt1m(opentime=r.openTime, openpr=r.open, hightpr=r.high, lowpr=r.low, closepr=r.close,
                        bustur=r.quoteAssetVolume, closetime=r.closeTime, busvolu=r.numTrades, busnum=r.volume,
                        actbustur=r.takerBuyBaseAssetVolume, actbusvolu=r.takerBuyQuoteAssetVolume)
        db.session.add(eth)
    # orders = binance.getorder()
    # for o in orders:
    #     odr = Order(ordertime = o.updateTime, orderid = o.orderId, side = o.side, price = o.price, origqty = o.origQty,
    #                 status = o.stat
    #     db.session.add(odr)
    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=False, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    wbuser = models.User
    user = wbuser.query.filter(wbuser.username==username).first()
    if user is not None:
        click.echo('更新用户')
        wbuser.username = username
        wbuser.set_password(password)
    else:
        click.echo('新增用户')
        wbuser = User(username=username, name='Guest')
        wbuser.set_password(password)
        db.session.add(wbuser)

    db.session.commit()
    click.echo('Done.')

@app.cli.command()
def geteth1m():
    last = Ethusdt1m.query.get(Ethusdt1m.query.count()).closetime
    command.onlinetime()
    if last is not None:
        now = datetime.now()
        a = 0
        while (now - last).seconds > 3600 or (now - last).days > 0:
            starttime = int(last.timestamp()*1000) + 1
            endtime = int(now.timestamp()*1000)
            res = bian.getstick(starttime=starttime, endtime=endtime, limit=600)
            coun = len(res)
            for r in res:

                eth = Ethusdt1m(opentime=r.openTime, openpr=r.open, hightpr=r.high, lowpr=r.low, closepr=r.close,
                                bustur=r.quoteAssetVolume, closetime=r.closeTime, busvolu=r.numTrades, busnum=r.volume,
                                actbustur=r.takerBuyBaseAssetVolume, actbusvolu=r.takerBuyQuoteAssetVolume)
                db.session.add(eth)
            db.session.commit()
            starstr = last
            last = Ethusdt1m.query.get(Ethusdt1m.query.count()).closetime
            now = datetime.now()
            endstr = datetime.strftime(last,'%Y-%m-%d %H:%M:%S')
            starstr = datetime.strftime(starstr, '%Y-%m-%d %H:%M:%S')
            print('增加时间从：%s到%s'%(starstr,endstr),"共%d条"%coun)
            a = a+coun

        endstr = datetime.strftime(last,'%Y-%m-%d %H:%M:%S')
        print('最新数据记录是：',endstr,' 本次共更新%d条数据'%a)
        return a
    print('没有查询到记录，运行flask forge构建数据库')
#
# @app.cli.command()
# def onlinetime():
#     now = datetime.now()
#     now = datetime.strftime(now,'%Y-%m-%d %H:%M:%S')
#     print('现在时间是：',now)
#     TimeServer = 'time.windows.com'  # 国家授时中心ip
#     Port = 123
#     def getTime():
#         TIME_1970 = 2208988800
#         client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         data = '\x1b' + 47 * '\0'
#         data = bytes(data, 'utf-8')
#         client.sendto(data, (TimeServer, Port))
#         data, address = client.recvfrom(1024)
#         data_result = struct.unpack('!12I', data)[10]
#         data_result -= TIME_1970
#         return data_result
#
#     tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.gmtime(getTime())
#     win32api.SetSystemTime(tm_year, tm_mon, tm_wday, tm_mday, tm_hour, tm_min, tm_sec, 0)
#     now = datetime.now()
#     now = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
#     print('更新后的时间是：', now)

