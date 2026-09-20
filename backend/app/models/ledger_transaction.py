from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base



class LedgerTransaction(Base):
    __tablename__ = "ledger_transactions"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    transfer_id: Mapped[int] = mapped_column(
        ForeignKey("transfers.id"),
        nullable=False,
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    transfer: Mapped["Transfer"] = relationship(
        back_populates="ledger_transaction",
    )

    entries: Mapped[list["LedgerEntry"]] = relationship(
        back_populates="ledger_transaction",
    )