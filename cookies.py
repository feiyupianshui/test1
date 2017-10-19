#!/use/bin/env python
#_*_coding:utf-8_*_
import requests
import json
import redis
import logging
from .settings import REDIS_URL

logger = logging.getLogger(__name__)
reds = redis.Redis.from_url(REDIS_URL, db=2, decode_responses=True)#把账密放到了db2，最后一个参数必须有，不然数据会变成byte形式，那就完全毁了。
login_url = 'http://dbfansub.com/user/login/?redirect_to=http%3A%2F%2Fdbfansub.com%2Ftvshow%2F8902.html'

def get_cookie(account, password):#这对参数在下面init_cookie()中对应着user:password这对键值
    s = requests.Session()
    payload = {
        'log': account,
        'pwd': password,
        'wp-submit': '登录',
        'redirect_to': 'http://dbfansub.com/tvshow/8902.html',
        'testcookie': '1'
    }
    response = s.post(login_url, data=payload)#模拟提交表单
    cookies = response.cookies.get_dict()
    logger.warning('获取Cookie成功！帐号为：%s' %account)
    return json.dumps(cookies)#如果不序列化，存入Redis后会变成Plain Text格式，后面取出来就没法用了

def init_cookie(red, spidername):#spidername在中间件中是用crawler.spider.name传入的
    redkeys = reds.keys()#登录帐号
    for user in redkeys:
        password = reds.get(user)#登录密码
        if red.get("%s:Cookies:%s--%s" % (spidername, user, password)) is None:
            cookie = get_cookie(user, password)#调用了上面的获取cookies函数
            red.set("%s:Cookies:%s--%s" % (spidername, user, password), cookie)#传入redis，但是red和reds是不一样的

#更新Cookie(upadate_cookie)和删除无法使用的帐号(remove_cookie)略，不写也不影响使用。
