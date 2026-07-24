from models.region_config import RegionConfig


REGIONS = {

    "identity": RegionConfig(
        start="Government of India",
        end="Address",
    ),

    "demographic": RegionConfig(
        start="Address",
        end="Aadhaar - Aam Aadmi",
    ),
}