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

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_DIR = os.path.join(ROOT_DIR, "logs")
APP_DIR = os.path.join(ROOT_DIR, "app")
WORK_DIR = os.path.join(ROOT_DIR, "work")
DATA_DIR = os.path.join(APP_DIR, "data")
ALLOWED_EXTENSIONS = {'java', 'go', 'js', 'py'}

JAVA_MAIN_TEMPLATE = os.path.join(DATA_DIR, "templates", "java_main_template")

CODE_CONF_FILE_NAME = "code_conf.json"
