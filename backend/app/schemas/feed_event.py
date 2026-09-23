from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FeedEventCreate(BaseModel):
    pond_id: int = Field(..., alias="pondId")
    fed_at: datetime = Field(..., alias="fedAt")
    feed_type: Optional[str] = Field(None, max_length=64, alias="feedType")
    amount_kg: Optional[float] = Field(None, alias="amountKg")
    operator_name: Optional[str] = Field(None, max_length=64, alias="operatorName")

    model_config = ConfigDict(populate_by_name=True)


class FeedEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    pond_id: int = Field(serialization_alias="pondId")
    fed_at: datetime = Field(serialization_alias="fedAt")
    feed_type: str = Field(serialization_alias="feedType")
    amount_kg: float = Field(serialization_alias="amountKg")
    operator_name: str = Field(serialization_alias="operatorName")
