from core.paddle_adapter import PaddleAdapter
from parsers.parser_registry import ParserRegistry


class ExtractionService:

    def __init__(
        self,
        adapter: PaddleAdapter,
        registry: ParserRegistry,
    ):
        self.adapter = adapter
        self.registry = registry

    def extract(self, image_path: str, document_type: str):
        document = self.adapter.extract(image_path)
        parser = self.registry.get(document_type)
        return parser.parse(document)