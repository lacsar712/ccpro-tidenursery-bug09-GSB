import math
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FeedEventCreate(BaseModel):
    pond_id: int = Field(..., alias="pondId")
    fed_at: datetime = Field(..., alias="fedAt")
    feed_type: str = Field(..., max_length=64, alias="feedType")
    amount_kg: float = Field(..., alias="amountKg")
    operator_name: str = Field(..., max_length=64, alias="operatorName")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("feed_type")
    @classmethod
    def validate_feed_type(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("饵料类型不能为空")
        return value

    @field_validator("operator_name")
    @classmethod
    def validate_operator(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("操作人不能为空")
        return value

    @field_validator("amount_kg")
    @classmethod
    def validate_amount(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("投喂量必须为有效数字")
        if value <= 0:
            raise ValueError("投喂量必须大于 0 千克")
        return value


class FeedEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    pond_id: int = Field(serialization_alias="pondId")
    fed_at: datetime = Field(serialization_alias="fedAt")
    feed_type: str = Field(serialization_alias="feedType")
    amount_kg: float = Field(serialization_alias="amountKg")
    operator_name: str = Field(serialization_alias="operatorName")
