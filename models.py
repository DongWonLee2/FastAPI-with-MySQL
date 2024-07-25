# 데이터베이스 테이블에 매핑되는 ORM 모델을 정의
'''
ORM 모델이란?
ORM(Object-Relational Mapping, 객체-관계 매핑)은 객체 지향 프로그래밍 언어를 사용하여 관계형 데이터베이스를 다루기 위한 기술입니다. ORM은 데이터베이스의 테이블을 클래스 형태로 매핑하여, 데이터베이스와 상호작용할 때 SQL 쿼리 대신 객체 지향 프로그래밍 언어의 객체를 사용할 수 있게 해줍니다. 이를 통해 개발자는 데이터베이스와의 상호작용을 더욱 직관적이고 쉽게 할 수 있습니다.

SQLAlchemy는 Python에서 널리 사용되는 ORM 라이브러리로, 관계형 데이터베이스와 상호작용하기 위해 사용됩니다. 
'''
# 필요한 모듈들을 임포트합니다.
from sqlalchemy import Boolean, Column, Integer, String
from database import Base

# User 테이블을 정의하는 클래스입니다.
class User(Base):
    __tablename__ = 'users'  # 이 클래스가 매핑될 데이터베이스 테이블 이름을 지정합니다.

    id = Column(Integer, primary_key=True, index=True)  # 사용자 ID(정수형 ID)로 기본 키이며 인덱스를 생성한다.
    username = Column(String(50), unique=True)  # 최대 50자 길이의 문자열로 사용자 이름을 저장하며, 유니크 속성을 가진다.
'''
유니크(Unique) 속성이란?
데이터베이스에서 유니크(Unique) 속성은 특정 컬럼의 값이 테이블 내에서 중복되지 않도록 보장하는 제약 조건입니다. 즉, 유니크 속성이 적용된 컬럼은 각각의 레코드(행)에서 항상 고유한 값을 가져야 합니다. 유니크 속성은 데이터의 무결성을 보장하고, 특정 컬럼의 값이 중복되지 않도록 하기 위해 사용됩니다. 예를 들어, 사용자 이름(username)이나 이메일 주소(email)와 같이 고유해야 하는 값들에 유니크 속성을 부여하면, 동일한 값이 여러 번 입력되는 것을 방지할 수 있습니다.
'''

# Post 테이블을 정의하는 클래스입니다.
class Post(Base):
    __tablename__ = 'posts'  # 테이블 이름을 지정합니다.

    id = Column(Integer, primary_key=True, index=True)  # 게시물 ID, 기본 키 속성
    title = Column(String(50))  # 최대 50자 길이의 문자열로 게시물 제목을 저장
    content = Column(String(100))  # 최대 100자 길이의 문자열로 게시물 내용을 저장
    user_id = Column(Integer)  # 게시물을 작성한 사용자 ID 저장
