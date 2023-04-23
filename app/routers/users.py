from fastapi import Depends, HTTPException, status, APIRouter
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(prefix="/userrr",tags = ['Users'])


@router.post("/", response_model=schemas.RespondUser, status_code=status.HTTP_201_CREATED)
def create_user(create_model: schemas.CreateUser, db: Session = Depends(get_db)):

    # HASH THE PASSWORD - USER PASSWORD
    encrypted_password = utils.pwd_context.hash(create_model.password)

    # NEW ENCRYPTED PASSWORD
    create_model.password = encrypted_password

    new_user = models.ORM_User(**create_model.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    if not new_user:
        raise HTTPException(status_code=status.HTTP_201_CREATED,
                            details="user was not created")
    return new_user

# RETRIEVING USERS

@router.get("/", response_model=list[schemas.RespondUser], status_code=status.HTTP_302_FOUND)
def retrieve_users(db: Session = Depends(get_db)):
    user_query = db.query(models.ORM_User).all()
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="users could not be retrieved ")
    return user_query

# RETRIEVE USER BY ID

@router.get("/{id}", response_model=schemas.RespondUser, status_code=status.HTTP_302_FOUND)
def find_user(id: int, db: Session = Depends(get_db)):
    finding_query = db.query(models.ORM_User).filter(
        models.ORM_User.id == (id))
    user = finding_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="users could not be retrieved ")
    return user

# DELETING USER

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    delete_query = db.query(models.ORM_User).filter(models.ORM_User.id == id)
    user_tbd = delete_query.first()
    delete_query.delete()
    db.commit()
    if not user_tbd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    return user_tbd


@router.put("/{id}", response_model=schemas.RespondUser)
def update(id: int, update_model: schemas.CreateUser, db: Session = Depends(get_db)):
    update_query = db.query(models.ORM_User).filter(models.ORM_User.id == id)
    update_query.update(update_model.dict(), synchronize_session=False)
    new_update = update_query.first()

    if not new_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{ id } does not exist")

    db.commit
    return new_update
