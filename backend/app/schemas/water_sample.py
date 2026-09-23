import math
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _require_finite(value: float, label: str) -> float:
    if not math.isfinite(value):
        raise ValueError(f"{label}必须为有效数字")
    return value


class WaterSampleCreate(BaseModel):
    pond_id: int = Field(..., alias="pondId")
    sampled_at: datetime = Field(..., alias="sampledAt")
    temp_c: float = Field(..., alias="tempC")
    salinity_ppt: float = Field(..., alias="salinityPpt")
    do_mg_l: float = Field(..., alias="doMgL")
    ph: float
    notes: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("temp_c")
    @classmethod
    def validate_temp_c(cls, value: float) -> float:
        return _require_finite(value, "水温")

    @field_validator("salinity_ppt")
    @classmethod
    def validate_salinity(cls, value: float) -> float:
        return _require_finite(value, "盐度")

    @field_validator("do_mg_l")
    @classmethod
    def validate_do(cls, value: float) -> float:
        _require_finite(value, "溶解氧")
        if value <= 0:
            raise ValueError("溶解氧必须大于 0 mg/L")
        return value

    @field_validator("ph")
    @classmethod
    def validate_ph(cls, value: float) -> float:
        _require_finite(value, "pH")
        if value < 6 or value > 9:
            raise ValueError("pH 必须在 6 到 9 之间")
        return value


class WaterSampleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    pond_id: int = Field(serialization_alias="pondId")
    sampled_at: datetime = Field(serialization_alias="sampledAt")
    temp_c: Optional[float] = Field(serialization_alias="tempC")
    salinity_ppt: Optional[float] = Field(serialization_alias="salinityPpt")
    do_mg_l: Optional[float] = Field(serialization_alias="doMgL")
    ph: Optional[float] = None
    notes: Optional[str] = None
