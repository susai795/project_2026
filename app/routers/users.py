from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select

from app.models.registration import Registration
from app.models.user import User
from app.data.db import get_session

user_router = APIRouter(prefix="/users",)


# GET /users
@user_router.get("", response_model=list[User])
def get_user(session: Session = Depends(get_session)):
    # Questa query diventerà solo: SELECT user.username FROM user (Funzionerà al 100%)
    db_users = session.exec(select(User)).all()

    return db_users


# POST /users
@user_router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: User, session: Session = Depends(get_session)):

    db_users = session.get(User, user.username)
    if db_users:
        raise HTTPException(status_code=400, detail="Username already exists")

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@user_router.get("/users/{username}", response_model=User)
def get_user(username: str, session: Session = Depends(get_session)):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.delete("", status_code=status.HTTP_200_OK)
def delete_all_users(session: Session = Depends(get_session)):
    registrations=session.exec(select(Registration)).all()
    for reg in registrations:
        session.delete(reg)

    users=session.exec(select(User)).all()
    for user in users:
        session.delete(user)
        session.commit()

    return {"Users deleted successfully"} #per messaggi, status_code 200_ok


@user_router.delete("/{username}", status_code=status.HTTP_200_OK)
def delete_user(username: str, session: Session = Depends(get_session)):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    registrations=session.exec(select(Registration).where(Registration.username==username))
    for reg in registrations:
        session.delete(reg)

    session.delete(user)
    session.commit()
    return {"User deleted successfully"}
