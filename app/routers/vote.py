from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy import true
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/votes", tags=['Votes'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def votes(vote: schemas.Vote, db: Session = Depends(database.get_db),
           current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,
                                       models.Votes.user_id == current_user.id)
    
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"user {current_user.id} already voted for post")
        
        new_vote = models.Votes(post_id= vote.post_id, user_id= current_user.id)

        db.add(new_vote)
        db.commit()

        return {'message': 'successfully added vote'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'vote does not exist')
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}