class AddressExtractor(BaseExtractor):

    def extract(
        self,
        region: OCRRegion,
    ) -> OCRField:
        ...