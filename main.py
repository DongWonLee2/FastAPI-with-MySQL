# FastAPI 애플리케이션의 주요 로직을 포함. 엔드포인트 정의와 데이터베이스 종속성 주입을 담당.
# FastAPI와 필요한 모듈들을 임포트합니다.
# HTTPException : HTTP 예외를 발생시키기 위해 사용. 특정 조건에서 클라이언트에게 HTTP 오류를 반환할 수 있다.
# Depends : 의존성 주입 시스템을 사용하기 위해 사용. 코드의 재사용성과 유지보수성을 높임.
# status : HTTP 상태 코드를 정의하는 데 사용됨.
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated # 타입에 대한 메타데이터를 추가해주는 기능. FastAPI의 의존성 주입과 함께 사용. Annotated(타입명, 메타데이터)
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

# FastAPI 인스턴스를 생성합니다.
app = FastAPI()

# 데이터베이스 테이블을 생성합니다. 만약 테이블이 이미 존재하면 이 코드는 무시됩니다.
models.Base.metadata.create_all(bind=engine)

# Post 모델의 기본 스키마를 정의합니다.
class PostBase(BaseModel): # model에서 작성한 기본 키는 제외
    title: str  # 게시물 제목
    content: str  # 게시물 내용
    user_id: int  # 사용자 ID

# User 모델의 기본 스키마를 정의합니다.
class UserBase(BaseModel): # model에서 작성한 기본 키는 제외
    username: str  # 사용자 이름

# 데이터베이스 세션을 생성하는 함수. 이를 요청 핸들러에 제공. 작업이 완료되면 세션을 닫아야 한다.
def get_db():
    db = SessionLocal() # 새 데이터베이스 세션을 생성한다.
    try:
        yield db  # 데이터베이스 세션을 호출자에게 반환합니다.
    finally:
        db.close()  # 세션을 닫습니다.

# FastAPI의 의존성 주입 시스템을 사용하여 데이터베이스 세션을 라우트 핸들러에 주입
db_dependency = Annotated[Session, Depends(get_db)]

# 엔드포인트 
'''
post.users의 전반적인 흐름
1. 클라이언트가 /users/ 경로로 HTTP POST 요청을 보냅니다. 요청 바디에는 username 필드가 포함됩니다.
2. create_user 함수가 호출되어 user 파라미터로 UserBase 모델의 인스턴스를 받습니다.
3. 데이터베이스 세션(db)을 의존성 주입을 통해 받아옵니다.
4. UserBase 모델의 데이터를 기반으로 models.User 클래스의 인스턴스를 생성합니다.
5. 생성된 인스턴스를 데이터베이스 세션에 추가하고, 커밋하여 데이터베이스에 저장합니다.
'''

@app.post("/users/", status_code=status.HTTP_201_CREATED) # 성공적으로 사용자 생성 시, HTTP 상태 코드 201(생성됨)을 반환
async def create_user(user: UserBase, db: db_dependency): # 비동기 함수, 새로운 사용자를 데이터베이스에 생성, UserBase, db_dependency 설정 
    # user.dict()는 UserBase 모델의 데이터를 딕셔너리 형태로 변환합니다. 
    # models.User(**user.dict()): 딕셔너리의 키-값 쌍을 models.User 클래스의 인스턴스 생성에 사용합니다. 이는 User 클래스의 인스턴스를 생성하여 데이터베이스 테이블에 삽입할 준비를 합니다.
    db_user = models.User(**user.dict())
    db.add(db_user) # 새로 생성된 db_user 객체를 데이터베이스 세션에 추가합니다.
    db.commit() # 데이터베이스 세션의 변경 사항을 커밋하여 실제로 데이터베이스에 반영합니다.
    
'''
get.users{user_id}의 전반적인 흐름
1. 클라이언트가 /users/{user_id} 경로로 HTTP GET 요청을 보냅니다. 요청 경로에는 user_id가 포함됩니다.
2. read_user 함수가 호출되어 user_id 파라미터로 사용자 ID를 받습니다.
3. 데이터베이스 세션(db)을 의존성 주입을 통해 받아옵니다.
4. User 모델에서 user_id에 해당하는 사용자를 조회합니다.
5. 조회된 사용자가 없으면 HTTP 404 오류를 발생시키고, "User not found" 메시지를 클라이언트에게 보냅니다.
6. 조회된 사용자가 있으면 해당 사용자 객체를 JSON 형식으로 클라이언트에게 반환합니다.
'''
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK) 
async def read_user(user_id:int, db: db_dependency): # 비동기 함수, 사용자 조회 함수
    user = db.query(models.User).filter(models.User.id == user_id).first() # 모든 레코드를 선택하는 쿼리 시작, user 모델의 id가 user_id와 일치하는지 필터링, 첫번째 레코드 반환
    if user is None:
        raise HTTPException(status_code=404, detail='User not found') # 조회된 사용자가 없을 경우 예외 발생
    return user # 조회된 사용자 객체 반환

'''
post.posts의 전반적인 흐름
1. 클라이언트가 /posts/ 경로로 HTTP POST 요청을 보냅니다. 요청 바디에는 게시물의 title, content, user_id 필드가 포함됩니다.
2. create_post 함수가 호출되어 post 파라미터로 PostBase 모델의 인스턴스를 받습니다.
3. 데이터베이스 세션(db)을 의존성 주입을 통해 받아옵니다.
4. PostBase 모델의 데이터를 기반으로 models.Post 클래스의 인스턴스를 생성합니다.
5. 생성된 인스턴스를 데이터베이스 세션에 추가하고, 커밋하여 데이터베이스에 저장합니다.
'''
@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency): # PostBase 모델의 데이터를 받아온다. 
    db_post = models.Post(**post.dict()) # 딕셔너리의 키-값 쌍을 인자로 넘겨 models.Post 클래스의 인스턴스 생성
    db.add(db_post) # 생성된 db_post 객체를 데이터베이스 세션에 추가
    db.commit() # 변경 사항 커밋하여 실제 데이터베이스에 반영

'''
get.posts의 전반적인 흐름
1. 클라이언트가 /posts/{post_id} 경로로 HTTP GET 요청을 보냅니다. 요청 경로에는 post_id가 포함됩니다.
2. read_post 함수가 호출되어 post_id 파라미터로 게시물 ID를 받습니다.
3. 데이터베이스 세션(db)을 의존성 주입을 통해 받아옵니다.
4. Post 모델에서 post_id에 해당하는 게시물을 조회합니다.
5. 조회된 게시물이 없으면 HTTP 404 오류를 발생시키고, "Post was not found" 메시지를 클라이언트에게 보냅니다.
6. 조회된 게시물이 있으면 해당 게시물 객체를 JSON 형식으로 클라이언트에게 반환합니다.
'''
@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency): # 게시물 ID로 데이터베이스에서 게시물 조회
    post = db.query(models.Post).filter(models.Post.id == post_id).first() # 쿼리 시작, 필터링, 조건에 맞는 첫 번째 레코드 반환
    if post is None:
        raise HTTPException(status_code=404, detail='Post was not found') # 예외 처리
    return post

'''
delete.posts의 전반적인 흐름
1. 클라이언트가 /posts/{post_id} 경로로 HTTP DELETE 요청을 보냅니다. 요청 경로에는 post_id가 포함됩니다.
2. delete_post 함수가 호출되어 post_id 파라미터로 게시물 ID를 받습니다.
3. 데이터베이스 세션(db)을 의존성 주입을 통해 받아옵니다.
4. Post 모델에서 post_id에 해당하는 게시물을 조회합니다.
5. 조회된 게시물이 없으면 HTTP 404 오류를 발생시키고, "Post was not found" 메시지를 클라이언트에게 보냅니다.
6. 조회된 게시물이 있으면 해당 게시물 객체를 데이터베이스 세션에서 삭제하고, 커밋하여 데이터베이스에서 삭제합니다.
'''
@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency): # 전달된 post_id에 해당하는 게시물 삭제
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first() # 쿼리 시작, 필터링, 첫 번째 레코드 반환
    if db_post is None:
        raise HTTPException(status_code=404, detail='Post was not found') # 예외 처리
    db.delete(db_post) # 조회된 게시물 객체를 데이터베이스 세션에서 삭제
    db.commit() # 변경사항 커밋