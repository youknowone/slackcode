
# coding: utf-8
import os
import subprocess
import threading
import codegen

import redis
rc = redis.StrictRedis()

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
        timeout = 8
    process = Process(*args)
    return process.run(timeout=timeout)

def error(code, *args):
    return '', ''
error.name = 'error'

def python2(code, *args):
    preset = '#coding: utf-8\nimport time,math,datetime,re,string,struct,difflib,unicodedata,calendar,collections,heapq,bisect,array,sets,weakref,types,new,copy,pprint,repr,numbers,cmath,decimal,fractions,random,itertools,functools,operator,csv,hashlib,hmac,md5,sha,io,json,urllib,urllib2,httplib,gettext,locale,requests,sys,bs4; argc=len(sys.argv); argv=sys.argv; del sys;\n'
    if 'import' in code or 'exec' in code:
        return '', 'rejected'
    return run('python', '-c', preset + code, *args)
python2.name = 'python2.7'
python2.help = '<https://docs.python.org/2/>'
python = python2

def python3(code, *args):
    preset = 'import time,math,datetime,re,string,struct,difflib,unicodedata,calendar,collections,heapq,bisect,array,weakref,types,copy,pprint,reprlib,enum,numbers,cmath,decimal,fractions,random,statistics,itertools,functools,operator,csv,hashlib,hmac,io,json,urllib,http,gettext,locale;\n'
    if 'import' in code or 'exec' in code:
        return '', 'rejected'
    return run('python3', '-c', preset + code, *args)
python3.name = 'python3.4'
python3.help = '<https://docs.python.org/3/>'

def ruby(code, *args):
    return run('ruby', '-e', code, *args)
ruby.name = 'ruby1.9'
ruby.help = '<https://www.ruby-lang.org/ko/documentation/>'

def aheui(code):
    return run('aheui', '-c', code, timeout=2)
aheui.name = u'아희'
aheui.help = u'<http://aheui.github.io/specification.ko/>'

def print_(code, *args):
    return code, ''
print_.name = 'print'

def c99(code):
    if '#include' in code:
        return '', 'rejected'
    codegen.render_c(code)
    out, err = run('clang', '-std=c99', '-o', 'tmp/c.out', 'tmp.c')
    if err:
        return out, err
    return run('tmp/c.out')
c99.name = 'c99'
c99.help = '<http://ko.wikipedia.org/wiki/C99>'

def cpp11(code):
    if '#include' in code:
        return '', 'rejected'
    codegen.render_cc(code)
    out, err = run('clang++', '-std=c++1y', '-o', 'tmp/cc.out', 'tmp.cc')
    if err:
        return out, err
    return run('tmp/cc.out')
cpp11.name = 'c++11'
cpp11.help = '<http://ko.wikipedia.org/wiki/C%2B%2B11>'

def rust(code):
    codegen.render_rust(code)
    out, err = run('rustc', '-o', 'tmp/rs.out', 'tmp.rs')
    if err:
        return out, err
    return run('tmp/rs.out')
rust.name = 'rust'
rust.help = '<http://www.rust-lang.org/>'

def save(code):
    try:
        key, value = code.split(' ', 1)
    except ValueError:
        return '', 'format: <key> <data>'
    rc.hset('slackcode', key, value)
    return '', ''
save.name = 'database'
save.help = 'save a sentence for the given key'

def load(code):
    value = rc.hget('slackcode', code)
    if not value:
        return '', u'`{}` is empty'.format(code)
    return value, ''
load.name = 'database'
load.help = 'load a sentence for the given key'

def call(code):
    try:
        key, arg = code.split(' ', 1)
    except ValueError:
        key, arg = code, ''
    value = rc.hget('slackcode', key)
    if not value:
        return '', u'`{}` is empty'.format(key)
    name, out, err = dispatch(value, arg)
    if name == 'error':
        return '', u'`{}` is not callable'.format(key)
    return out, err
call.name = 'database'
call.help = 'What you see is what it does'

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
'ruby': ruby,
'aheui': aheui,
u'아희': aheui,
'c': c99,
'c99': c99,
'c++': cpp11,
'cpp': cpp11,
'c++11': cpp11,
'c++14': cpp11,
'rust': rust,
'langhelp': help,
u'언어도움': help,
'save': save,
u'쓰기': save,
'load': load,
u'읽기': load,
'call': call,
u'실행': call,
'print': print_,
}
help.help = u'언어 이름을 넣으면 약간의 설명이... ' + ' '.join(sorted(machines.keys()))

def dispatch(text, *args):
    try:
        tag, code = text.split(' ', 1)
    except ValueError:
        tag = text
        code = ''
    tag = tag[1:]
    if tag and tag[0] == '!':
        out, err = call(' '.join([tag[1:], code]))
        if not out and err.endswith(' is empty') or err.endswith(' is not callable'):
            return call.name, '', ''
        return call.name, out, err
    machine = machines.get(tag, error)
    out, err = machine(code, *args)
    try:
        name = machine.name
    except:
        name = tag
    return name, out, err

