from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import EntryDirection
from app.db.base import Base



class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="ck_ledger_entry_amount_positive",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("ledger_transactions.id"),
        nullable=False,
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=False,
    )

    direction: Mapped[EntryDirection] = mapped_column(
        Enum(EntryDirection),
        nullable=False,
    )

    amount: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    ledger_transaction: Mapped["LedgerTransaction"] = relationship(
        back_populates="entries",
    )