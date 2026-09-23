from sqlalchemy.orm import Session

from app.models import Customer
from app.schemas.customer import CustomerCreate


def create_customer(
    db: Session,
    data: CustomerCreate,
) -> Customer:

    customer = Customer(
        name=data.name,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer