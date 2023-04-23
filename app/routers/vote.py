
from fastapi import Depends, HTTPException, status, APIRouter
from .. import schemas, models,database,oauth2


router = APIRouter(prefix = "/votes", tags=['Vote'])

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(create_vote:schemas.Vote, db: database.SessionLocal = Depends(database.get_db),current_user: int = Depends(oauth2.get_current_user)):
    post=db.query(models.ORM_Post).filter (models.ORM_Post.id == create_vote.update_id).first()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"the post with id : {create_vote.update_id} does not exist")



    vote_query = db.query(models.Vote).filter(models.Vote.update_id == create_vote.update_id, models.Vote.user_id ==current_user.id)
    found_vote = vote_query.first()
    if (create_vote.dir==1):
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail= f" user  {current_user.id} has already voted on post {create_vote.update_id}")
        new_vote=models.Vote(update_id = create_vote.update_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return "successfully added vote"
    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = " vote does not exist ")
        vote_query.delete(synchronize_session= False)
        db.commit()
        return {"message" : "successfully deleted vote"}

