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
from common.utils import utils, constants

logger = logging.getLogger()


class CodeConfig:

    def __init__(self, unique_id, cos_object=None):
        self.config_file = os.path.join(constants.WORK_DIR, unique_id + ".json")
        logger.debug("Config Filename: "+self.config_file)
        self.cos_object = cos_object

    def save_conf(self, conf_dict):
        logger.debug("In _create_conf")
        if os.path.exists(self.config_file):
            configuration = utils.convert_json_to_dict(self.config_file)
        else:
            configuration = {}
        for conf_key in conf_dict:
            configuration[conf_key] = conf_dict[conf_key]
        utils.convert_dict_to_json(configuration, self.config_file)
        if self.cos_object:
            self.cos_object.upload_file(self.config_file)

    def get_conf(self, conf_key):
        logger.debug("In Get Config")
        if self.cos_object:
            self.cos_object.download_file(self.config_file)
        configuration = utils.convert_json_to_dict(self.config_file)
        return configuration.get(conf_key)
