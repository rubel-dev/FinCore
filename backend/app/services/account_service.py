from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.enums import AccountStatus
from app.models import Account, Customer
from app.schemas.account import AccountCreate


def create_account(
    db: Session,
    data: AccountCreate,
) -> Account:

    customer = db.get(Customer, data.customer_id)

    if customer is None:
        raise ValueError("Customer does not exist")

    existing_account = db.scalar(
        select(Account).where(
            Account.customer_id == data.customer_id
        )
    )

    if existing_account is not None:
        raise ValueError("Customer already has an account")

    account = Account(
        customer_id=customer.id,
        currency=data.currency.upper(),
        status=AccountStatus.ACTIVE,
        balance_snapshot=0,
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return account