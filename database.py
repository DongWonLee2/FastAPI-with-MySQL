# 데이터베이스 연결 및 세션을 설정
'''
데이터베이스 세션이란?
데이터베이스 세션은 애플리케이션과 데이터베이스 간의 일시적인 연결을 의미합니다. 세션을 통해 애플리케이션은 데이터베이스에 쿼리를 보내고, 데이터를 삽입, 업데이트, 삭제할 수 있으며, 이러한 작업이 완료되면 세션을 종료하여 리소스를 해제합니다.

세션의 역할
상태 관리:
세션은 데이터베이스와의 연결 상태를 관리합니다. 이는 데이터베이스와의 연결이 열려 있는 동안 상태를 유지하고, 작업이 완료되면 연결을 닫는 것을 포함합니다.

트랜잭션 관리:
세션은 트랜잭션을 관리합니다. 트랜잭션은 데이터베이스의 일련의 작업을 하나의 단위로 묶어 처리하는 것을 의미합니다. 세션은 트랜잭션을 시작하고, 필요한 경우 커밋(commit)하거나 롤백(rollback)할 수 있습니다.

쿼리 실행:
세션은 데이터베이스에 쿼리를 실행하고 결과를 반환받는 역할을 합니다. 이를 통해 애플리케이션은 데이터베이스의 데이터를 읽고 쓸 수 있습니다.
'''
# 필요한 라이브러리들을 임포트합니다.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 데이터베이스 URL을 정의합니다. 여기에는 데이터베이스 타입, 사용자명, 비밀번호, 호스트, 포트, 데이터베이스 이름이 포함되어야 합니다.
URL_DATABASE = 'mysql+pymysql://root:07069@localhost:3306/blogapplication'  # 실제 데이터베이스 URL로 대체해야 합니다.

# 데이터베이스와 상호작용(연결)하기 위한 엔진을 생성합니다.
engine = create_engine(URL_DATABASE)

# 데이터베이스 세션을 생성하는 세션 메이커를 설정합니다. 세션은 데이터베이스와 상호작용하는 동안 상태를 관리합니다.
# autocommit=False: 세션에서 자동으로 커밋하지 않도록 설정합니다.
# autoflush=False: 세션이 자동으로 플러시되지 않도록 설정합니다. 플러시 : 변경을 감지하고 변경내용이 데이터베이스에 반영되는 것
# bind=engine: 세션을 데이터베이스 엔진에 바인딩합니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모든 ORM(객체 관계 매핑) 모델이 상속받을 기본 클래스입니다. 이 클래스를 상속받아 데이터베이스 테이블에 매핑되는 클래스를 정의할 수 있습니다.
Base = declarative_base()
