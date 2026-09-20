from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import AccountStatus
from app.db.base import Base



class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
        unique=True,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    status: Mapped[AccountStatus] = mapped_column(
        Enum(AccountStatus),
        nullable=False,
        default=AccountStatus.ACTIVE,
    )

    # Store money in the smallest unit.
    # Example: ৳10.50 -> 1050 poisha
    balance_snapshot: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="account",
    )