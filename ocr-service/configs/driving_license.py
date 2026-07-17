from models.region_config import RegionConfig


REGIONS = {

    "identity": RegionConfig(
        start="DL No.",
        end="ADDRESS",
    ),

    "address": RegionConfig(
        start="ADDRESS",
        end="Sign.",
    ),
}