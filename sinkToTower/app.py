# -*- coding: utf-8 -*-
#!/bin/python
#########
## Post an AWS Cloud Trail Event as Cloud Event to the Ansible Tower API
## @author markito, 2020
#########

from flask import Flask, send_file
from flask import request
from io import BytesIO
import traceback
import logging
import qrcode
import signal
import sys
import json
import uuid
import os
import requests
import urllib.request
from urllib import parse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def encode():
    print(request.data)
    try:
        # extract event body from cloud events
        raw_data = request.data
        json_data = json.loads(raw_data)
        ce_body = json_data["Body"]
        json_body = json.loads(ce_body)

        logging.debug('JSON Body: {}'.format(json_body))

        eventName = json_body["detail"]["eventName"]
        print(eventName)

        result = post({"eventName":eventName})
        message = "Job started. \n {0}".format(result)

        print(message)
        return message
    except Exception as e:
        return "Error sending or parsing the request: {0}".format(e)

'''
 Read <code>ENDPOINT</code> <code>T_USER</code> and <code>T_PASS</code> from
 environment variables to authenticate against Ansible Tower and post
 <code>data</code> as payload
'''
def post(data):
    ENDPOINT=os.environ.get('ENDPOINT', "https://student1.sean-tower.rhdemo.io/api/v2/job_templates/Knative%20-%20AWS%20Report++Default/launch/")
    USER=os.environ.get('T_USER')
    PASS=os.environ.get('T_PASS')

    headers = {'Content-type': 'application/json'}
    r = requests.post(ENDPOINT,data=json.dumps(data),headers=headers, auth=(USER, PASS))
    return r.text

def signal_term_handler(signal, frame):
    logging.warning('Received SIGTERM')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_term_handler)
    app.run(host='0.0.0.0', port=8080)
