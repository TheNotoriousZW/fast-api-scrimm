from sqlalchemy import delete, func
from app import oauth2
from .. import models, schemas
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal, get_db
from typing import Optional, List
from . import vote

router = APIRouter(prefix="/posts",
                   tags=['posts'])

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #return {"data": posts}

    print(limit)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Votes.post_id).label("likes")).join(models.Votes,
         models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = list ( map (lambda x : x._mapping, posts) )

    
    return results
    
@router.post("/", response_model=schemas.Post)
def post(post: schemas.CreatePost, db: Session = Depends(get_db), 
         current_user: int = Depends(oauth2.get_current_user),
         ):

    #cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""", 
    # (post.title, post.content, post.published))

    #new_post = cursor.fetchone()

    #conn.commit()

    new_post = models.Post(owner_id=current_user.id,
    **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    #posts = cursor.fetchone()
    
    
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Votes.post_id).label("likes")).join(models.Votes,
         models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")
    
    return  post

    
    
@router.delete("/{id}")
def del_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    #deleted_post = cursor.fetchone()

    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")
    
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail=f"you are not permitted to delete {deleted_post.owner_id} post")
    

    db.delete(deleted_post)
    db.commit()
    #conn.commit()
   
    return {"detail": f"post has been deleted"}

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user) ):
    #cursor.execute("""UPDATE posts SET title = %s , content = %s WHERE id = %s RETURNING *""", (post.title, post.content, str(id)))

    #post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post doesnt exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail=f"you are not permitted to update {post.owner_id} post")
    
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
    #conn.commit()

    return  post_query.first()
