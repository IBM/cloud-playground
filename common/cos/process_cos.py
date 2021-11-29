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
from os import environ
from common.cos import cos

logger = logging.getLogger(__name__+'.py')


def get_cos_client():
    logger.debug("Initialize COS")
    cos_endpoint = environ.get('COS_ENDPOINT')
    if not cos_endpoint:
        logger.error('No valid COS endpoint specified')
        return None

    api_key = environ.get('APIKEY')
    if not api_key:
        logger.error('No IAM API key found')
        return None

    cos_bucket = environ.get('COS_BUCKET')
    if not cos_bucket:
        logger.error('Must specify a destination bucket')
        return None

    cos_instance_id = environ.get('COS_INSTANCE_ID')
    if not cos_instance_id:
        logger.error('No COS instance ID found')
        return None

    iam_endpoint = environ.get('IAM_ENDPOINT')
    if not iam_endpoint:
        logger.error('No IAM endpoint specified')
        return None

    try:
        cos_client = cos.CloudObjectStorage(
            api_key=api_key,
            instance_id=cos_instance_id,
            iam_endpoint=iam_endpoint,
            cos_endpoint=cos_endpoint,
            cos_bucket=cos_bucket)
    except Exception as ex:
        logger.error(str(cos.COSError))
        logger.error(str(ex))
        return None

    return cos_client
