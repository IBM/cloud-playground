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

import logging
import os

from common.code_handlers.code import Code
from common.code_handlers.code_config import CodeConfig
from common.code_handlers.go import Go
from common.code_handlers.java import Java
from common.code_handlers.nodejs import NodeJS
from common.code_handlers.python import Python
from common.utils import constants
from common.cos import process_cos

logger = logging.getLogger()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in constants.ALLOWED_EXTENSIONS


def get_results(unique_id):
    code_obj = Code(unique_id)
    results = code_obj.get_output()
    status = code_obj.get_status()
    return results, status


def get_code(unique_id, file=None):
    logger.debug("in get_code_object")
    # file_loc = get_file_loc(unique_id)
    if file is None:
        logger.debug("No file provided so getting details from config")
        # logger.debug(file_loc)
        cos_cli=process_cos.get_cos_client()
        code_config = CodeConfig(unique_id,cos_cli)
        script_file = code_config.get_conf("file_name")
    else:
        logger.debug("File is provided")
        script_file = file.filename
    logger.debug(script_file)
    if script_file.endswith("py"):
        code_obj = Python(unique_id, file)
    elif script_file.endswith("java"):
        code_obj = Java(unique_id, file)
    elif script_file.endswith("go"):
        code_obj = Go(unique_id, file)
    elif script_file.endswith("js"):
        code_obj = NodeJS(unique_id, file)
    else:
        raise Exception("Unknown File Name type")
    return code_obj
