
# coding: utf-8
import html
import json
import redis
import traceback
import engine
from flask import Flask, request

from settings import *

app = Flask(__name__)

@app.route('/hook', methods=('POST',))
def hook():
    """
    token, team_id, team_domain, channel_id, channel_name, timestamp, user_id, user_name, text
    """
    try:
        print(request.form.get('user', None))
        text = request.form.get('text', None)
        text = html.unescape(text)
        if text:
            name, out, err = engine.dispatch(text)
            outtext = ''
            if out.strip():
                outtext += '```' + out + '```'
            print(out)
            print(err)
            if err.strip():
                outtext += '\nerror:\n```' + err + '```'
            return json.dumps({'text': outtext, 'username': name})
    except Exception as e:
        traceback.print_exc()
        return json.dumps({'text': str(request.form) + '\n\n' + traceback.format_exc()})
    return ''
