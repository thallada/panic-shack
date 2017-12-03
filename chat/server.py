import calendar
import logging
import subprocess
from datetime import datetime, timedelta

import redis
from flask import Flask, request

conn = redis.Redis('localhost')
app = Flask(__name__)


@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


@app.route('/chat/', methods=['POST'])
def send_chat():
    if request.method == 'POST':
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        recent_ips = conn.hgetall("minecraft_chat_recent_ips")
        now = datetime.utcnow()
        if ip in recent_ips:
            if (now - datetime.fromutctimestamp(recent_ips[ip])) > timedelta.seconds(30):
                recent_ips[ip] = calendar.timegm(now.utctimetuple())
        if request.form.get('email', None):
            return 'Text was entered into honeypot!', 200
        if not request.form.get('say-text', None):
            return 'No message to send!', 422
        if request.form.get('say-username', None):
            subprocess.call(['/usr/bin/screen', '-S', 'mc-panic-shack', '-p', '0', '-X', 'stuff',
                             '/say [{}]: {}\015'.format(request.form['say-username'], request.form['say-text'])])
        else:
            subprocess.call(['/usr/bin/screen', '-S', 'mc-panic-shack', '-p', '0', '-X', 'stuff',
                             '/say {}\015'.format(request.form['say-text'])])
        return 'Sending chat: ' + request.form.get('say-username', '') + ': ' + request.form['say-text']


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="8888")
