from datetime import date as Date
from typing import Literal
from pydantic import BaseModel, field_validator

class FlightRequest(BaseModel):
    origin: str | None = None
    destination: str | None = None
    date: Date | None = None
    travel_class: Literal["economy", "business", "first"] | None = None

    @field_validator("date")
    @classmethod
    def validate_date(cls, value):
        if value is not None and value < Date.today():
            raise ValueError("Flight date cannot be in the past")
        return value