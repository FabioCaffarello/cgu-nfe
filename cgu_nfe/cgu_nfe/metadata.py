import hashlib
from datetime import date, timedelta


class GenerateProcessingMetadata:
    def __init__(self, bot_name):
        self.bot_name = bot_name
        self.processing_data = dict()
        self._get_input_date()
        self._generate_processsing_metadata()

    def _get_processing_date(self):
        processing_date = date.today()
        self.processing_data["processingDate"] = processing_date.strftime("%Y-%m-%d")
        return processing_date

    def _get_input_date(self):
        processing_date = self._get_processing_date()
        source_date_reference = processing_date + timedelta(days=-30)
        self.processing_data["sourceDateReference"] = source_date_reference.strftime("%Y-%m-%d")

    def _generate_processsing_metadata(self):
        processingId = "".join([
            self.bot_name,
            self.processing_data["processingDate"]
        ])
        self.processing_data["processingId"] = hashlib.md5(processingId.encode("utf-8")).hexdigest()
