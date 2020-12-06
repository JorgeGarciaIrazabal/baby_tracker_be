from datetime import timedelta
from http import HTTPStatus

from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from passlib.hash import sha256_crypt
from pydantic import BaseModel

from src.app import Session
from src.env import JWT_SECRET
from src.models import Baby, PParent, ParentWithToken, Parent


class Settings(BaseModel):
    authjwt_secret_key: str = JWT_SECRET


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()


def encrypt_password(password: str) -> str:
    return sha256_crypt.hash(password)


def validate_password(password, parent: Parent):
    if not sha256_crypt.verify(password, parent.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED.value, detail="Unauthorized"
        )


def get_parent_from_token(auth: AuthJWT) -> Parent:
    session = Session()
    try:
        email = auth.get_jwt_subject()
        auth.jwt_required()
        return session.query(Parent).filter_by(email=email).one()
    finally:
        session.close()


def generate_parent_with_token(parent: Parent, auth: AuthJWT) -> ParentWithToken:
    access_token = auth.create_access_token(
        subject=parent.email, expires_time=timedelta(days=365)
    )
    parent.password = "~~~"
    return ParentWithToken(parent=PParent.from_orm(parent), token=access_token)


def validate_baby_relationship(auth: AuthJWT, baby_id: int):
    parent = get_parent_from_token(auth)
    session = Session()
    try:
        baby: Baby = session.query(Baby).get(baby_id)
        if parent.id not in baby.parent_ids:
            raise HTTPException(
                status_code=HTTPStatus.PRECONDITION_FAILED.value,
                detail="No relationship with baby",
            )

    finally:
        session.close()
