import logging
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


@app.route('/chat/', methods=['GET', 'POST'])
def send_chat():
    if request.method == 'POST':
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
    else:
        app.logger.info('Hello, world!')
        return 'Hello, world!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port="8888")
