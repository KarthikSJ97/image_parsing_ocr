from dataclasses import dataclass

@dataclass
class RegionConfig:
    start: str | None = None
    end: str | None = None