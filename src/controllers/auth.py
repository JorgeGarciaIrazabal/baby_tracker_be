from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.app import app, get_db
from src.models import PParent, Parent, ParentWithToken
from src.services.auth import encrypt_password, generate_parent_with_token, validate_password


@app.put(
    "/sign_in",
    response_model=ParentWithToken,
    tags=["api"],
    response_model_exclude={"parent.password"},
)
def sign_in(
    email: str, password: str, auth: AuthJWT = Depends(), db: Session = Depends(get_db)
):
    parent = db.query(Parent).filter_by(email=email).one()
    validate_password(password, parent)
    return generate_parent_with_token(parent, auth)


@app.post("/sign_up", response_model=ParentWithToken, tags=["api"])
def sign_up(
    pydantic_parent: PParent, db: Session = Depends(get_db), auth: AuthJWT = Depends()
):
    pydantic_parent.password = encrypt_password(pydantic_parent.password)
    parent = Parent(**pydantic_parent.dict())
    db.add(parent)
    db.commit()
    return generate_parent_with_token(parent, auth)
