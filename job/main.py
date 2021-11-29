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
import logging.config
from os import environ
from common import config
from common.utils import utils
from common.code_handlers import code_gen

logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)
logger=logging.getLogger()

def run_job():

    #Export the Job Env variables
    ce_data = environ.get('CE_DATA')
    if not ce_data:
        logger.error('No CE_DATA Received')
        return -1

    data_dict=utils.convert_json_to_dict(json_string=ce_data)
    environ["COS_BUCKET"]=data_dict["notification"]["bucket_name"]
    filename=data_dict["notification"]["object_name"]

    #Get the unique id
    unique_id=filename.split(".",1)[0].split("_",1)[1]
    logger.debug("Unique Id: "+unique_id)

    #Execute the User's file
    code_obj=code_gen.get_code(unique_id)
    if code_obj:
        code_obj.run()
    else:
        return -1


if __name__ == "__main__":
    exit(run_job())
