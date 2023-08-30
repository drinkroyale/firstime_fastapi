from .. import models, schema, utility, oauth2
from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from sqlalchemy import func
router = APIRouter(
    prefix="",
    tags=['Posts']
)


# @router.get("/", response_model=List[schema.Post])
@router.get("/", response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              Limit: int = 10, skip: int = 2, search: Optional[str] = ""):
    print(Limit)
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(
                                         models.Vote, models.Vote.post_id == models.Post.id,
                                         isouter=True).group_by(models.Post.id).filter(
                                         models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    
    return posts


@router.post("/createpost", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(yellowMixtape: schema.PostCreate, db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (yellowMixtape.title, yellowMixtape.content, yellowMixtape.published))
    # new_post = cursor.fetchone()
    # connection.commit()

    new_post = models.Post(owner_id=user_id.id, **yellowMixtape.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@router.get("/post/{id}", response_model=schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
             user_id: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s; """, (str(id),))
    # curs_id = cursor.fetchone()
    # connection.commit()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(
            models.Vote, models.Vote.post_id == models.Post.id,
            isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"post with {id} is not found.")
    return post


@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # backspace = cursor.fetchone()
    # connection.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/updatepost/{id}", response_model=schema.Post)
def update_post(id: int, upd_post: schema.PostCreate, db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s 
    #                WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()
    
    saving_query = db.query(models.Post).filter(models.Post.id == id)
    post = saving_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")
        
    saving_query.update(upd_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)

    return post
