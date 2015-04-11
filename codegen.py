#!/usr/bin/env python

import sys
import jinja2

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('.'))

def render_c(code): 
    template = env.get_template('template.c')
    rendered = template.render(main='int main' in code or 'void main' in code, code=code)
    with open('tmp.c', 'w') as f:
        f.write(rendered)

