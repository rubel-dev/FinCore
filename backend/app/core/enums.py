import enum


class AccountStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"


class TransferStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class EntryDirection(str, enum.Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class LedgerTransactionType(str, enum.Enum):
    INITIAL_FUNDING = "INITIAL_FUNDING"
    TRANSFER = "TRANSFER"