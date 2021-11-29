import logging

from common.code_handlers.code import Code
from common.utils import utils, constants

logger = logging.getLogger()


class Python(Code):

    def __init__(self, file_path, file):
        logger.debug("In Python Code")
        super().__init__(file_path, file)

    def validate(self):
        pass

    def run(self):
        logger.debug("Run Python code")
        super().download()
        logger.debug("python3", self.code_file_path, ">", self.out_file)
        process = utils.run(["python3", self.code_file_path], location_to_run=constants.WORK_DIR, out_file=self.out_file)
        logger.debug("Sending back the session")
        self.complete(process)
