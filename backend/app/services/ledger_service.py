from app.core.enums import EntryDirection
from app.models import LedgerEntry


def validate_balanced_entries(
    entries: list[LedgerEntry],
) -> None:
    total_debit = sum(
        entry.amount
        for entry in entries
        if entry.direction == EntryDirection.DEBIT
    )

    total_credit = sum(
        entry.amount
        for entry in entries
        if entry.direction == EntryDirection.CREDIT
    )

    if total_debit != total_credit:
        raise ValueError("Ledger transaction is not balanced")