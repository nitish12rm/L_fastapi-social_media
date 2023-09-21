from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from ..database import engine, get_db
from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
    
)
@router.get("/",response_model=list[schemas.PostOut_vote])
def get_post( db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),limit: int = 10,skip: int = 0,search: Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # post = db.query(models.Post,func.count(models.vote.post_id).label("votes")).join(models.vote,models.vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id)

    # return post 
    posts = db.query(models.Post, func.count(models.vote.post_id).label("votes")).join(
        models.vote, models.vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostOut) 
def create_post(posts: schemas.PostCreate,db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)) :

    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,
    #                (posts.title ,posts.content ,posts.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    #ORM METHOD:
    # created_post = models.Post(title=posts.title,content = posts.content, is_published=posts.published)
    #or
    print(current_user.email)
    created_post = models.Post(owner_id = current_user.id,**posts.model_dump())
    #niche ke codes DB ko update karne ke liye hai
    ###########
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    #############
    return created_post 

@router.get('/{id}',status_code=status.HTTP_302_FOUND,response_model=schemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id)))
    # post = cursor.fetchone()
    #ORM IMPLEMENTATION:
    post  = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found!")
    return post

@router.delete('/{id}')
def delete_post(id: int,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post= cursor.fetchone()
    # conn.commit()
    
    #ORM IMLEMENTATION
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deletd_post = deleted_post_query.first()
    if deletd_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found!")
    if deletd_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform such action")
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}',response_model=schemas.PostOut)
def update_post(id:int,updated_post:schemas.PostCreate,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",(posts.title,posts.content,posts.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    #ORM IMPLEMENTATION
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exists!")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform such action")
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    return  post_query.first()