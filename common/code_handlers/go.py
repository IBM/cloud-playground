import logging

from common.code_handlers.code import Code
from common.utils import utils

logger = logging.getLogger()


class Go(Code):

    def __init__(self, file_path, unique_id):
        super().__init__(file_path, unique_id)

    def validate(self):
        pass

    def run(self):
        logger.debug("Run Go code")
        super().download()
        logger.debug("go" + "run" + self.code_file_path + ">" + self.out_file)
        process = utils.run(["go", "run", self.code_file_path], location_to_run=constants.WORK_DIR, out_file=self.out_file)
        logger.debug("Sending back the session")
        self.complete(process)
