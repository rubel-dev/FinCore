from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import AccountStatus


class AccountCreate(BaseModel):
    customer_id: int
    currency: str = Field(min_length=3, max_length=3)


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    currency: str
    status: AccountStatus
    balance_snapshot: int
    created_at: datetime