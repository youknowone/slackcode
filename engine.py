
# coding: utf-8
import os
import subprocess
import threading

class Process(object):
    def __init__(self, *args):
        self.args = args
        self.result = '', ''

    def run(self, timeout=5):
        def target():
            self.process = subprocess.Popen(self.args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.result = self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
            return '', 'timeout'
        return self.result

def run(*args, **kwargs):
    if 'timeout' in kwargs:
        timeout = kwargs['timeout']
    else:
        timeout = 5
    process = Process(*args)
    return process.run(timeout=timeout)

def error(code):
    return '', ''
error.name = 'error'

def python2(code):
    preset = 'import time,math,datetime,re,string,struct,difflib,unicodedata,calendar,collections,heapq,bisect,array,sets,weakref,types,new,copy,pprint,repr,numbers,cmath,decimal,fractions,random,itertools,functools,operator,csv,hashlib,hmac,md5,sha,io,json,urllib,urllib2,httplib,gettext,locale,requests;\n'
    if 'import' in code or 'exec' in code:
        return '', 'rejected'
    return run('python', '-c', preset + code)
python2.name = 'python2.7'
python2.help = '<https://docs.python.org/2/>'
python = python2

def python3(code):
    preset = 'import time,math,datetime,re,string,struct,difflib,unicodedata,calendar,collections,heapq,bisect,array,weakref,types,copy,pprint,reprlib,enum,numbers,cmath,decimal,fractions,random,statistics,itertools,functools,operator,csv,hashlib,hmac,io,json,urllib,http,gettext,locale;\n'
    if 'import' in code or 'exec' in code:
        return '', 'rejected'
    return run('python3', '-c', preset + code)
python3.name = 'python3.4'
python3.help = '<https://docs.python.org/3/>'

def aheui(code):
    return run('../rpaheui/aheui-c', '-c', code, timeout=2)
aheui.name = u'아희'
aheui.help = u'<http://aheui.github.io/specification.ko/>'

def rot13(code):
    import string
    table = string.maketrans( 
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
    try:
        return string.translate(code.encode('utf-8'), table).decode('utf-8'), ''
    except:
        return '', 'invalid roman sentence'
rot13.name = 'rot13'
rot13.help = '<http://ko.wikipedia.org/wiki/ROT13>'

def help(code):
    try:
        machine = machines[code]
    except KeyError:
        return u'지원하지 않는 언어입니다.', ''
    try:
        name = machine.name
    except AttributeError:
        name = code
    try:
        help = machine.help
    except AttributeError:
        help = u'도움말이 없습니다.'
    return name + ': ' + help, ''
help.name = u'도움말'
machines = {
'py': python,
'py2': python2,
'py3': python3,
'python': python,
'python2': python2,
'python3': python3,
'aheui': aheui,
u'아희': aheui,
'rot13': rot13,
'langhelp': help,
u'언어도움': help,
}
help.help = u'언어 이름을 넣으면 약간의 설명이... ' + ' '.join(sorted(machines.keys()))

def dispatch(text):
    try:
        tag, code = text.split(' ', 1)
        tag = tag[1:]
    except ValueError:
        tag = None
        code = ''
    if not code.strip():
        tag = None
    machine = machines.get(tag, error)
    out, err = machine(code)
    try:
        name = machine.name
    except:
        name = tag
    return name, out, err

