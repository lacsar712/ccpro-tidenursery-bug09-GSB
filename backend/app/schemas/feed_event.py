from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FeedEventCreate(BaseModel):
    pond_id: int = Field(..., alias="pondId")
    fed_at: datetime = Field(..., alias="fedAt")
    feed_type: str = Field(..., max_length=64, alias="feedType")
    amount_kg: float = Field(..., alias="amountKg", allow_inf_nan=False)
    operator_name: Optional[str] = Field(None, max_length=64, alias="operatorName")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("feed_type")
    @classmethod
    def feed_type_must_not_be_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("饵料类型不能为空")
        return v

    @field_validator("amount_kg")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("投喂量必须大于 0 千克")
        return v


class FeedEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    pond_id: int = Field(serialization_alias="pondId")
    fed_at: datetime = Field(serialization_alias="fedAt")
    feed_type: str = Field(serialization_alias="feedType")
    amount_kg: float = Field(serialization_alias="amountKg")
    operator_name: str = Field(serialization_alias="operatorName")
