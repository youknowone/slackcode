#!/usr/bin/env python

import sys
import jinja2

from jinja2 import Environment, FileSystemLoader, Markup
env = Environment(loader=FileSystemLoader('.'))

def render_c(code): 
    template = env.get_template('template.c')
    rendered = template.render(main='int main' in code or 'void main' in code, code=Markup(code).unescape())
    with open('tmp.c', 'w') as f:
        f.write(rendered)

def render_cc(code):
    template = env.get_template('template.cc')
    rendered = template.render(main='int main' in code or 'void main' in code, code=Markup(code).unescape())
    with open('tmp.cc', 'w') as f:
        f.write(rendered)

def render_rust(code):
    template = env.get_template('template.rs')
    rendered = template.render(main='fn main' in code, code=Markup(code).unescape())
    with open('tmp.rs', 'w') as f:
        f.write(rendered)

