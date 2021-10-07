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

import os
import logging
import time

from common.code_handlers.code_config import CodeConfig
from common.utils import utils, constants
from common.cos import process_cos

logger = logging.getLogger()

class Code(object):
    def __init__(self, unique_id, file=None):
        self.out_file = os.path.join(constants.WORK_DIR, unique_id + ".log")
        self._cos_client = process_cos.get_cos_client()
        self._code_config = CodeConfig(unique_id, self._cos_client)
        if file:
            self.file_contents = file.read().decode()
            file_extension = os.path.splitext(file.filename)[1]
            target_file="job_" + unique_id + file_extension
            self.code_file_path = os.path.join(constants.WORK_DIR, target_file)
            utils.create_file(self.code_file_path)
            utils.create_file(self.out_file)
            self._code_config.save_conf({"file_name": target_file,
                                         "status": "created"})
        else:
            logger.debug("Getting config data from file")
            file_name = self._code_config.get_conf("file_name")
            self.code_file_path = os.path.join(constants.WORK_DIR, file_name)
        #Timeout in seconds (30min * 60)
        self.timeout = 1800

    def download(self):
        if self._cos_client:
            self._cos_client.download_file(file=self.code_file_path)
        logger.debug("File downloaded at: ",self.code_file_path)

    def start(self):
        utils.string_to_file(self.file_contents, self.code_file_path)
        if self._cos_client:
            self._cos_client.upload_file(file=self.code_file_path)
        self._code_config.save_conf({"status": "started"})

    def complete(self, session):
        logger.debug("Complete")
        for i in range(0, self.timeout):
            logger.debug(f"Checking for completion {i} time")
            time.sleep(1)
            if self._cos_client:
                self._cos_client.upload_file(self.out_file)
            if session.poll() is not None:
                self._code_config.save_conf({"status": "completed"})
                break

    def get_output(self):
        if self._cos_client:
            self._cos_client.download_file(self.out_file, download_location=self.out_file + "_temp")
        output = utils.file_to_string(self.out_file + "_temp")
        return output

    def get_status(self):
        logger.debug("Get Status")
        return self._code_config.get_conf("status")
