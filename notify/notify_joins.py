#!/usr/bin/env python
# Read the Minecraft server log and diff it against the server log it saw last. If there any new joins in the diff, send
# a notification.
import codecs
import os
import re
from datetime import datetime

import requests

from secrets import IFTTT_WEBHOOK_KEY_TYLER, IFTTT_WEBHOOK_KEY_KAELAN

LOG_FILENAME = '/srv/minecraft-panic-shack/logs/latest.log'
OLD_LOG_FILENAME = '/srv/minecraft-panic-shack/logs/last-read.log'
USERNAME_BLACKLIST = ['anarchyeight', 'kinedactyl']
IFTTT_EVENT_NAME = 'user_joined_panic_shack'


def read_log(filename):
    with codecs.open(filename, encoding='utf-8') as log:
        return log.readlines()


def save_log(filename, lines):
    with codecs.open(filename, 'w', encoding='utf-8') as log:
        log.writelines(lines)


if __name__ == '__main__':
    if (datetime.fromtimestamp(os.path.getmtime(LOG_FILENAME)) >
            datetime.fromtimestamp(os.path.getmtime(OLD_LOG_FILENAME))):
        new_log = read_log(LOG_FILENAME)
        old_log = read_log(OLD_LOG_FILENAME)
        if new_log[0] != old_log[0]:
            # A log rotate occured
            old_log = []
        if len(new_log) > len(old_log):
            for new_line in new_log[len(old_log):]:
                match = re.match('[\[][0-9:]+[\]]\s[\[]Server thread/INFO]: (\S+) joined the game', new_line)
                if match:
                    username = match.group(1)
                    if username not in USERNAME_BLACKLIST:
                        # IFTTT does not support sharing Applets anymore :(
                        r = requests.post(
                            'https://maker.ifttt.com/trigger/{}/with/key/{}'.format(IFTTT_EVENT_NAME,
                                                                                    IFTTT_WEBHOOK_KEY_TYLER),
                            data={'value1': username})
                        r = requests.post(
                            'https://maker.ifttt.com/trigger/{}/with/key/{}'.format(IFTTT_EVENT_NAME,
                                                                                    IFTTT_WEBHOOK_KEY_KAELAN),
                            data={'value1': username})
        save_log(OLD_LOG_FILENAME, new_log)
