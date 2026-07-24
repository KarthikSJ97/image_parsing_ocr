from pydantic import BaseModel


class AadhaarSchema(BaseModel):
    aadhaar_number: str | None = None

    name: str | None = None

    dob: str | None = None

    yob: str | None = None

    gender: str | None = None

    address: str | None = None