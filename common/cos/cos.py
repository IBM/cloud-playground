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

from ibm_boto3.session import Session
from ibm_botocore.client import Config, ClientError
from pathlib import PurePath

logger = logging.getLogger()

class CloudObjectStorage:
    def __init__(self, api_key=None, instance_id=None, iam_endpoint=None,
                 cos_endpoint=None, cos_bucket=None):
        try:
            self.cos_endpoint = cos_endpoint
            self.session = Session(
                ibm_api_key_id=api_key,
                ibm_service_instance_id=instance_id,
                ibm_auth_endpoint=iam_endpoint)
        except ClientError as be:
            logger.error("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            logger.exception("Unable to Init CloudObjectStorage: {0}".format(e))
        self.cos_bucket = cos_bucket

    # Method to create an item in the given bucket by passing file contents(as bytes)
    def create_file(self, item_name=None, item_contents=None):
        try:
            cos = self.session.resource(
                service_name='s3',
                endpoint_url=self.cos_endpoint,
                config=Config(signature_version='oauth')
            )
            response = cos.Object(self.cos_bucket, item_name).put(
                Body=item_contents
            )
            return response
        except ClientError as be:
            logger.error("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            logger.exception("Unable to Create file: {0}".format(e))

    # Method to get the item contents
    def get_item(self, item_name=None):
        try:
            cos = self.session.resource(
                service_name='s3',
                endpoint_url=self.cos_endpoint,
                config=Config(signature_version='oauth')
            )
            response = cos.Object(self.cos_bucket, item_name).get()
            return response
        except ClientError as be:
            logger.error("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            logger.exception("Unable to get items from COS: {0}".format(e))

    # Method to upload a file in the given bucket
    def upload_file(self, file=None, target_filename=None):
        try:
            cos = self.session.resource(
                service_name='s3',
                endpoint_url=self.cos_endpoint,
                config=Config(signature_version='oauth')
            )

            if not (target_filename is None):
                item_name = target_filename
            else:
                item_name = PurePath(file).name

            response = cos.Bucket(self.cos_bucket).upload_file(file, item_name)
            return response
        except ClientError as be:
            logger.error("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            logger.exception("COS File Upload Failed: {0}".format(e))

    # Method to download a file from the given bucket using file/item name
    def download_file(self, file, download_location=None):
        try:
            cos = self.session.resource(
                service_name='s3',
                endpoint_url=self.cos_endpoint,
                config=Config(signature_version='oauth')
            )
            item_name = PurePath(file).name
            if not (download_location is None):
                target_file=download_location
            else:
                target_file=file
            logger.info("Object name: "+item_name)
            logger.info("Download Location: "+target_file)
            response = cos.Object(self.cos_bucket, item_name).download_file(
                Filename=target_file
            )
            return response
        except ClientError as be:
            logger.error("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            logger.exception("COS Download Failed: {0}".format(e))

    # Method to delete a file from the given bucket
    def delete_file(self, file=None):
        try:
            cos = self.session.resource(
                service_name='s3',
                endpoint_url=self.cos_endpoint,
                config=Config(signature_version='oauth')
            )
            response = cos.Bucket(self.cos_bucket).delete_objects(
                Delete={
                    'Objects': [
                        {'Key': file}
                    ],
                    'Quiet': True
                    },
                MFA='string',
                RequestPayer='requester'
            )
            if 'Errors' in response.keys():
                raise COSError
        except ClientError as be:
            logger.error("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            logger.exception("COS Delete Failed: {0}".format(e))


class COSError(Exception):
    """Exception class for errors when interacting with COS."""
    pass
