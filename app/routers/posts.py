

from typing import Optional
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy import func
from .. import schemas, models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/sqlalchposts", tags=['posts'])


# POST METHOD. CREATING POST
# def find_length():
#     total_index = len(my_posts)
#     return(total_index + int(1))


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.RespondPost)
async def create_post(createpost_model: schemas.CreatePost, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO updates(title,comment,published) VALUES(%s,%s,%s) RETURNING * """,
    #                (post.title,post.comment,post.published))
    # new_post = models.ORM_Post(title=create_post.title,comment=create_post.comment,published= create_post.published)
    print(current_user.id)
    new_post = models.ORM_Post(
        owner_id=current_user.id, **createpost_model.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#     # new_post = cursor.fetchone()
# #     post_dict = post.dict()
# #     post_dict['id']= find_length()
# #     my_posts.append(post_dict)
#     if not new_post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="posts can not be found",
#         )
#     conn.commit()
#     print("created data:",new_post)
#     return new_post


# @router.get("/")
# async def root():
#     return {"message": "Hello World"}


# READING POSTS
@router.get('/', response_model=list[schemas.RespondPost])
# ADDED QUERY PARAMETERS (LIMIT)
async def read_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(current_user.email)
    read_posts_query = db.query(models.ORM_Post).filter(
        models.ORM_Post.comment.contains(search))
    # I YOU WANT TO SEE ONLY POSTS MADE BY A PARTICULAR USER
    # .filter(
    #     models.ORM_Post.owner_id == current_user.id)
    
    updates = read_posts_query.limit(limit).offset(skip).all()

    # results_query = db.query(models.ORM_Post, func.count(models.ORM_Vote.update_id).label("votes")).join(
    #     models.ORM_Vote, models.ORM_Vote.update_id == models.ORM_Post.id, isouter=True).group_by(models.ORM_Post.id)
    
    # results = results_query.all()
    # if not read_posts_query:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="posts were not found",
    #     )

    return updates
#     cursor.execute("""SELECT * FROM updates""")
#     my_posts=cursor.fetchall()
#     post = my_posts
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="posts could not be found",
#         )
#     return post


# READING SINGLE POST
# def find_index(id:int):

#     for n in (my_posts):
#         if n ['id']== id:
#             return n

@router.get('/{id}', response_model=schemas.RespondPost)
async def read_single_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    single_post_query = db.query(models.ORM_Post).filter(
        models.ORM_Post.id == id)
    single_post = single_post_query.first()
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with with id : {id} was not found")

    # IF YOU WANT TO GET SINGLE POST ONLY MADE BY THE CURRENT USER

    # if single_post.owner_id != current_user.id:
    #     raise HTTPException(status.HTTP_403_FORBIDDEN,
    #                         detail='you are not authorized to perform this action ')
    return single_post

#     cursor.execute("""SELECT* FROM updates WHERE id=(%s)""",str((id)))
#     post =cursor.fetchone()
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"the 'id':{id} could not be found",
#         )
#     return post


# DELETE POST
# def find_tbd(id:int):
#     for n , m in enumerate(my_posts):
#         if m['id']==id:
#             print( f"{m} was deleted")
#             return n


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    delete_query = db.query(models.ORM_Post).filter(models.ORM_Post.id == id)
    deleted_post = delete_query.first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail='you can only delete comments made by you ')
    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
#     cursor.execute("""DELETE FROM updates WHERE id=(%s) RETURNING *""",str((id)))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     # my_posts.pop(post)
#     if not deleted_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")
#     return (f'post id: {id} was successfully deleted')


# UPDATE POST
# def update_index(id:int):
#     for n,m in enumerate(my_posts):
#         if m['id']==id:
#             return n

@router.put('/{id}', response_model=schemas.RespondPost)
async def update_post(id: int, update_model: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.ORM_Post).filter(models.ORM_Post.id == id)
    post_query.update(update_model.dict(), synchronize_session=False)
    updated_post = post_query.first()
    db.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{ id } does not exist")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail='you can not make changes to this post ')
    return updated_post
#     # index = update_index(id)
#     cursor.execute("""UPDATE updates SET title=%s,comment=%s WHERE id=%s RETURNING *""", (post.title,post.comment,str(id)))
#     update_post = cursor.fetchone()
#     conn.commit()
#     # post_dict = post.dict()
#     #post_dict['id']= id
#     # my_posts[index] = post_dict
#     if post== None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")
#     print (update_post)
#     return update_post
