from sqlalchemy.orm import Session

from app.core.enums import (
    AccountStatus,
    EntryDirection,
    LedgerTransactionType,
    TransferStatus,
)
from app.models import (
    Account,
    LedgerEntry,
    LedgerTransaction,
    Transfer,
)
from app.schemas.transfer import TransferCreate
from app.services.ledger_service import validate_balanced_entries


def create_transfer(
    db: Session,
    data: TransferCreate,
) -> Transfer:
    try:
         
        sender = db.get(Account, data.sender_account_id)
        receiver = db.get(Account, data.receiver_account_id)

        
        validate_transfer(
            sender=sender,
            receiver=receiver,
            data=data,
        )

        
        transfer = Transfer(
            sender_account_id=sender.id,
            receiver_account_id=receiver.id,
            amount=data.amount,
            currency=data.currency,
            status=TransferStatus.PENDING,
        )

        db.add(transfer)
        db.flush()

         
        ledger_transaction = LedgerTransaction(
            transfer_id=transfer.id,
            transaction_type=LedgerTransactionType.TRANSFER
        )

        db.add(ledger_transaction)
        db.flush()

         
        entries = [
            LedgerEntry(
                transaction_id=ledger_transaction.id,
                account_id=sender.id,
                direction=EntryDirection.DEBIT,
                amount=data.amount,
            ),
            LedgerEntry(
                transaction_id=ledger_transaction.id,
                account_id=receiver.id,
                direction=EntryDirection.CREDIT,
                amount=data.amount,
            ),
        ]

        
        validate_balanced_entries(entries)

        db.add_all(entries)

        
        sender.balance_snapshot -= data.amount
        receiver.balance_snapshot += data.amount

        
        transfer.status = TransferStatus.COMPLETED

        
        db.commit()
        db.refresh(transfer)

        return transfer

    except Exception:
        db.rollback()
        raise

def validate_transfer(
    sender: Account | None,
    receiver: Account | None,
    data: TransferCreate,
) -> None:

    if sender is None:
        raise ValueError("Sender account does not exist")

    if receiver is None:
        raise ValueError("Receiver account does not exist")

    if sender.id == receiver.id:
        raise ValueError(
            "Sender and receiver accounts must be different"
        )

    if sender.status != AccountStatus.ACTIVE:
        raise ValueError("Sender account is not active")

    if receiver.status != AccountStatus.ACTIVE:
        raise ValueError("Receiver account is not active")

    if sender.currency != data.currency:
        raise ValueError(
            "Sender account currency does not match"
        )

    if receiver.currency != data.currency:
        raise ValueError(
            "Receiver account currency does not match"
        )

    if sender.balance_snapshot < data.amount:
        raise ValueError("Insufficient balance")
    

