import logging
import shlex
import subprocess
import unicodedata

from flask import Flask, request

app = Flask(__name__)


@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


def sanitize_input(input):
    input = "".join(ch for ch in input if unicodedata.category(ch)[0] != "C")
    return shlex.quote(input.replace('^', ''))


@app.route('/chat/', methods=['POST'])
def send_chat():
    if request.method == 'POST':
        if request.form.get('email', None):
            return 'Text was entered into honeypot!', 200
        if not request.form.get('say-text', None):
            return 'No message to send!', 422
        if request.form.get('say-username', None):
            subprocess.call([
                '/usr/bin/screen', '-S', 'mc-panic-shack', '-p', '0', '-X', 'stuff',
                '/say [{}]: {}\015'.format(
                    sanitize_input(request.form['say-username']),
                    sanitize_input(request.form['say-text']))
            ])
        else:
            subprocess.call([
                '/usr/bin/screen', '-S', 'mc-panic-shack', '-p', '0', '-X', 'stuff',
                '/say {}\015'.format(sanitize_input(request.form['say-text']))
            ])
        return 'Sending chat: ' + request.form.get('say-username', '') + ': ' + request.form['say-text']

if __name__ == "__main__":
    app.run(host='0.0.0.0', port="8888")
