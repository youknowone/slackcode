
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

def run(*args):
    process = Process(*args)
    return process.run()

def error(code):
    return '', ''
error.name = 'error'

def python(code):
    preset = 'import time,math,sys,requests;\n'
    if 'import' in code:
        return '', 'rejected'
    return run('python', '-c', preset + code)
python.name = 'python2.7'

def dispatch(text):
    try:
        tag, code = text.split(' ', 1)
        tag = tag[1:]
    except ValueError:
        tag = None
        code = ''
    if not code.strip():
        tag = None
    machine = {
        'py': python,
        'py2': python,
        'python': python,
        'python2': python,
    }.get(tag, error)
    out, err = machine(code)
    return machine.name, out, err

