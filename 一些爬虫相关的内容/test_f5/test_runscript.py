import time
import json
import pprint
import requests
import random

interface = 'http://127.0.0.1:18089'
interface = 'http://8.130.11.250:18089'

# import vthread
# @vthread.pool(10)
def run(only_info=False):
    url = interface + '/run_script'
    data = {
        "scripts": ["var some = 333", "some + 333"],
        "only_script": True,
    }
    s = requests.post(url, data=data).json()
    print(s)

for i in range(10):
    run()