# -*- coding: utf-8 -*-
from datetime import datetime
from pyquery import PyQuery
import urllib2
import pickle


def is_numeric(value):
    try:
        return isinstance(long(value), long)
    except ValueError:
        return False


def un_shorted_url(url):
    origin_url = url
    try:
        resp = urllib2.urlopen(url)
        code = resp.getcode()
        if code == 200:
            origin_url = resp.url
    except Exception as e:
        print 'Error.un_shorted_url() {}'.format(str(e))
    finally:
        return origin_url


def get_title(url):
    title = ''
    try:
        html = urllib2.urlopen(url).read()
        if html:
            raw_message = PyQuery(html)
            if raw_message:
                raw_title = raw_message('title')
                if raw_title:
                    title = raw_title.text()
    except Exception as e:
        print 'Error.get_title() {}'.format(str(e))
    finally:
        return title


def save_cookie(data):
    return pickle.dumps(data)


def load_cookie(data):
    return pickle.loads(data)


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    pass
