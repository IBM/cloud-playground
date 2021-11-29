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

import json
import os
import logging
import subprocess


logger = logging.getLogger()



def run_good(cmd, location_to_run=None):
    current_dir = ""
    # if isinstance(cmd, str):
    #     cmd = shlex.split(cmd)

    if location_to_run:
        logger.debug("Running the command {} in the dir {}".format(str(cmd), location_to_run))
        current_dir = os.getcwd()
        os.chdir(location_to_run)
    else:
        logger.debug("Running the command {}".format(str(cmd)))
    session = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = session.communicate()
    if location_to_run:
        os.chdir(current_dir)

    if stderr:
        status = False
        cmd_output = stderr.decode('utf-8')
    else:
        status = True
        cmd_output = stdout.decode('utf-8')
    return status, cmd_output


def run(cmd, location_to_run=None, out_file=None):
    current_dir = ""
    # if isinstance(cmd, str):
    #     cmd = shlex.split(cmd)

    if location_to_run:
        logger.debug("Running the command {} in the dir {}".format(str(cmd), location_to_run))
        current_dir = os.getcwd()
        os.chdir(location_to_run)
    else:
        logger.debug("Running the command {}".format(str(cmd)))
    if out_file:
        out_file_obj = open(out_file, "w")
        session = subprocess.Popen(cmd, stdout=out_file_obj, stderr=out_file_obj)
    else:
        session = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if location_to_run:
        os.chdir(current_dir)
    return session


def run_as_daemon(cmd, outfile, location_to_run=None):
    current_dir = ""
    if location_to_run:
        logger.debug("Running the command {} in the dir {}".format(str(cmd), location_to_run))
        current_dir = os.getcwd()
        os.chdir(location_to_run)
    else:
        logger.debug("Running the command {}".format(str(cmd)))
    if not os.path.exists(outfile):
        create_file(outfile)
    cmd = "nohup " + cmd + " >> " + outfile + " &"
    print(cmd)
    session = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process_id = session.pid
    # stdout, stderr = session.communicate()
    if location_to_run:
        os.chdir(current_dir)

    # if stderr:
    #     status = False
    #     cmd_output = stderr.decode('utf-8')
    # else:
    #     status = True
    #     cmd_output = stdout.decode('utf-8')
    # status, cmd_output
    return process_id


def run_not_work(cmd, location_to_run=None):
    current_dir = ""
    if location_to_run:
        logger.debug("Running the command {} in the dir {}".format(str(cmd), location_to_run))
        current_dir = os.getcwd()
        os.chdir(location_to_run)
    else:
        logger.debug("Running the command {}".format(str(cmd)))
    print(' '.join(cmd))
    session = subprocess.Popen(cmd, shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
    # stdout, stderr = session.communicate()
    process_id = session.pid
    if location_to_run:
        os.chdir(current_dir)

    # if stderr:
    #     status = False
    #     cmd_output = stderr.decode('utf-8')
    # else:
    #     status = True
    #     cmd_output = stdout.decode('utf-8')
    return process_id


def create_file(file_path, permission=None):
    """
    :param file_path: path of the file to be created
    :param permission: the permission that needs to be set. As in linux chmod (like 755, 600, 777)
    :return:
    """
    logger.debug("Create file in the location " + file_path)
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        logger.debug("Creating the dir " + file_dir)
        os.makedirs(file_dir, exist_ok=True)
        if os.path.exists(file_dir):
            logging.debug("The location is created")
        else:
            raise FileNotFoundError(file_dir + " is not creatable")
    else:
        logging.debug("The location is already present")

    f = open(file_path, 'w+')
    f.close()
    if permission:
        os.chmod(file_path, permission)


def delete_file(file_path):
    os.unlink(file_path)


def configure_logger(log_config=None, stream_everything=False):
    """
    A function to get the logger module configured with params
    """
    primary_handler = log_config.get('log_handler', None)
    primary_handler_format = log_config['handler_format']
    primary_handler_date_format = log_config['date_format']
    if primary_handler == 'console':
        handler = logging.StreamHandler()
    elif primary_handler == 'file':
        if not log_config['log_path'].startswith("/"):
            log_path = os.path.join(
                log_config['log_path'])
        else:
            log_path = log_config['log_path']
        if not os.path.exists(log_path):
            create_file(log_path)
        handler = logging.FileHandler(log_path)
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter(
        primary_handler_format,
        datefmt=primary_handler_date_format)
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.handlers = []
    logger.addHandler(handler)
    if stream_everything:
        steam_handler = logging.StreamHandler()
        steam_handler.setFormatter(formatter)
        logger.addHandler(steam_handler)
    logger.setLevel(str(log_config['log_level']).upper())
    return logger


def file_to_string(file_path, as_bytes=False):
    file_contents = ""
    try:
        if as_bytes:
            with open(file_path, 'rb') as f_handler:
                file_contents = f_handler.read()
        else:
            with open(file_path) as f_handler:
                file_contents = f_handler.read()
    except FileNotFoundError:
        logging.warning("The file is not found - " + file_path)
    except Exception:
        logging.warning("Error while reading the file - " + file_path)
    return file_contents


def convert_dict_to_json(dictionary, json_file=None, indent=0):
    json_string = json.dumps(dictionary, indent=indent)
    if json_file:
        string_to_file(json_string, json_file)
    else:
        return json_string


def convert_json_to_dict(json_file=None, json_string=None):
    if json_file is not None:
        if not os.path.exists(json_file):
            return {}
        with open(json_file) as f:
            json_string = f.read()
    return json.loads(json_string)


def string_to_file(string_contents, file_path):
    with open(file_path, "w") as text_file:
        text_file.write(str(string_contents))


# def is_process_running(process_id):
#     run_process = psutil.Process(process_id)
#     status = run_process.is_running()
#     if not status:
#         logger.debug("The process is not running")
#     else:
#         logger.debug("The process is running")
#     return status
