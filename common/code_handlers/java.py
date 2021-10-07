import glob
import logging
import os

from common.code_handlers.code import Code
from common.utils import utils, constants

logger = logging.getLogger()


class Java(Code):

    def __init__(self, file_path, unique_id):
        logger.debug("Initialize Java Class")
        super().__init__(file_path, unique_id)

    def validate(self):
        pass

    @staticmethod
    def _get_class_name(file_dir):
        logger.debug("_get_class_name")
        class_files = glob.glob(file_dir + "/*.class")
        if len(class_files) == 0:
            return ""
        elif len(class_files) == 1:
            cur_class_file = class_files[0]
        else:
            cur_class_file = max(class_files, key=os.path.getctime)
        logger.debug("The current class File - " + cur_class_file)
        class_name = os.path.splitext(os.path.basename(cur_class_file))[0]
        logger.debug(class_name)
        return class_name

    def run(self):
        logger.debug("Run the Java code")
        if " void main(" in self.file_contents:
            super().start()
        else:
            java_template = utils.file_to_string(constants.JAVA_MAIN_TEMPLATE)
            java_file = java_template.replace("<DO_IMPORT_REPLACE>", "")
            java_file = java_file.replace("<DO_CODE_REPLACE>", self.file_contents)
            utils.string_to_file(java_file, self.code_file_path)
            super().start()

        file_location = os.path.join(constants.WORK_DIR, self.unique_id)

        status, out = utils.run(["javac", self.file_name], location_to_run=file_location)
        if status:
            class_name = self._get_class_name(file_location)
            status, out = utils.run(["java", class_name], location_to_run=file_location)
        self._status = status
        self._op = out.split("\n")
        self.complete()
