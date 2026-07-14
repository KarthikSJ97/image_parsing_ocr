class PANParser(BaseParser):

    REGIONS = PanConfig.REGIONS

    def preprocess(self):
        super().preprocess()

    def extract(self):

        return {
            "pan_number": ...,
            "name": ...,
            "father_name": ...,
            "date_of_birth": ...
        }