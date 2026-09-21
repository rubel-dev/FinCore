from sqlalchemy.orm import Session

from app.core.enums import (
    AccountStatus,
    EntryDirection,
    LedgerTransactionType,
)
from app.models import (
    Account,
    LedgerEntry,
    LedgerTransaction,
)
from backend.app.services.ledger_service import validate_balanced_entries


def fund_account(
    db: Session,
    system_account: Account,
    target_account: Account,
    amount: int,
) -> LedgerTransaction:
    try:
        validate_funding(
            system_account=system_account,
            target_account=target_account,
            amount=amount,
        )

        
        ledger_transaction = LedgerTransaction(
            transfer_id=None,
            transaction_type=LedgerTransactionType.INITIAL_FUNDING,
        )

        db.add(ledger_transaction)
        db.flush()

        
        entries = [
            LedgerEntry(
                transaction_id=ledger_transaction.id,
                account_id=system_account.id,
                direction=EntryDirection.DEBIT,
                amount=amount,
            ),
            LedgerEntry(
                transaction_id=ledger_transaction.id,
                account_id=target_account.id,
                direction=EntryDirection.CREDIT,
                amount=amount,
            ),
        ]
        validate_balanced_entries(entries)
        db.add_all(entries)

       
        system_account.balance_snapshot -= amount
        target_account.balance_snapshot += amount

        
        db.commit()
        db.refresh(ledger_transaction)

        return ledger_transaction

    except Exception:
        db.rollback()
        raise

def validate_funding(
    system_account: Account,
    target_account: Account,
    amount: int,
) -> None:
    if amount <= 0:
        raise ValueError("Funding amount must be positive")

    if system_account.id == target_account.id:
        raise ValueError(
            "System and target accounts must be different"
        )

    if system_account.status != AccountStatus.ACTIVE:
        raise ValueError("System account is not active")

    if target_account.status != AccountStatus.ACTIVE:
        raise ValueError("Target account is not active")

    if system_account.currency != target_account.currency:
        raise ValueError("Account currencies must match")

    if system_account.balance_snapshot < amount:
        raise ValueError("System account has insufficient balance")