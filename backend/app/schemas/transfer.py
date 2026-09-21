

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from  app.core.enums import TransferStatus


class TransferCreate(BaseModel):
    sender_account_id: int
    receiver_account_id: int

    amount: int = Field(gt = 0)
    currency: str = Field(
        min_length = 3,
        max_length = 3
    )


class TransferResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: int
    sender_account_id: int
    receiver_account_id: int
    amount: int
    currency: str
    status: TransferStatus
    created_at: datetime