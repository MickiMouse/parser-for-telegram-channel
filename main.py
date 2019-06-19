import os
import datetime

while True:
    if datetime.datetime.now().time() == datetime.time(0, 0, 0):
        os.system('python parse_analytics.py')
        os.system('python bot.py')
