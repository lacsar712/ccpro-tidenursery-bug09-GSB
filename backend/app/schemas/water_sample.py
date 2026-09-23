from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WaterSampleCreate(BaseModel):
    pond_id: int = Field(..., alias="pondId")
    sampled_at: datetime = Field(..., alias="sampledAt")
    temp_c: Optional[float] = Field(None, alias="tempC")
    salinity_ppt: Optional[float] = Field(None, alias="salinityPpt")
    do_mg_l: Optional[float] = Field(None, alias="doMgL")
    ph: Optional[float] = None
    notes: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class WaterSampleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    pond_id: int = Field(serialization_alias="pondId")
    sampled_at: datetime = Field(serialization_alias="sampledAt")
    temp_c: float = Field(0.0, serialization_alias="tempC")
    salinity_ppt: float = Field(0.0, serialization_alias="salinityPpt")
    do_mg_l: float = Field(0.0, serialization_alias="doMgL")
    ph: float = 0.0
    notes: Optional[str] = None
