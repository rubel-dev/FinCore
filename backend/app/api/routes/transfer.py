
from fastapi import APIRouter, Depends, HTTPException, status

from app.db.session import get_db
from app.schemas.transfer import TransferCreate, TransferResponse
from sqlalchemy.orm import Session

from app.services.transfer_service import create_transfer

router = APIRouter(
    prefix = "/transfers",
    tags=["Transfer"]
)


@router.post(
    "",
    response_model=TransferResponse,
    status_code=status.HTTP_201_CREATED
)
def transfer_money(
    data: TransferCreate,
    db: Session = Depends(get_db)
) -> TransferResponse:
    try:
        transfer = create_transfer(
            db=db,
            data=data
        )
        return transfer

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc
    