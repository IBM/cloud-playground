# -*- mode:python; coding:utf-8 -*-

# Copyright (c) 2021 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_cors import CORS
from common.code_handlers import code_gen
from common.utils import constants, utils

app = Flask(__name__)
CORS(app)
if app.config["ENV"] == "dev":
    config.from_object("config.DevelopmentConfig")
    stream_log = True
else:
    app.config.from_object("config.ProductionConfig")
    stream_log = False
logger = utils.configure_logger(app.config["LOG_DETAILS"])


@app.route("/")
def test_con():
    """
    A basic API to test the connection to the back-end.
    If the status is 200 then the connection is successful
    :return: {message: ''} and status is 200
    """
    resp = jsonify({'message': 'Able to connect to CPL back-end. Use URI (code) to send the file'})
    resp.status_code = 200
    return resp


@app.route('/code', methods=['POST'])
def process_code():
    """
    This API if used for accepting the code files and run them
    Validates if the file is a valid one and the extension is accepted.
    Once validated it saves the file in the system and executes it.

    The return message is send back in the message
    :return: {message: ''} and status is 201 (400 in-case of Failure)
    """
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    file = request.files['file']
    unique_id = request.values.get("id")
    logger.debug(unique_id)
    if not unique_id:
        resp = jsonify({'message': 'Please specify an Unique ID to run'})
        resp.status_code = 400
        return resp

    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and code_gen.allowed_file(file.filename):
        code_obj=code_gen.get_code(unique_id, file)
        if code_obj:
            code_obj.start()
            resp = jsonify({'message': "Triggered the script"})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'message': 'Failed to upload in COS'})
            resp.status_code = 400
            return resp
    else:
        resp = jsonify({'message': 'Allowed file types are ' + ', '.join(constants.ALLOWED_EXTENSIONS)})
        resp.status_code = 400
        return resp


@app.route('/result', methods=['GET'])
def process_results():
    """
    This API if used for accepting the code files and run them
    Validates if the file is a valid one and the extension is accepted.
    Once validated it saves the file in the system and executes it.

    The return message is send back in the message
    :return: {message: ''} and status is 201 (400 in-case of Failure)
    """
    unique_id = request.values.get("id")
    logger.debug(unique_id)

    if not unique_id:
        resp = jsonify({'message': 'Please specify an Unique ID to run'})
        resp.status_code = 400
        return resp
    output, status = code_gen.get_results(unique_id)
    logger.debug("The status is - " + str(status))
    resp = jsonify({'message': status, 'output': output, 'etc': "600", 'elapsed_time': ''})
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    app.run()
