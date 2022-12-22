# account_book
가계부사용 및 수정을 위한 API

# requirement
```bash
docker
docker-compose
```
도커를 사용하여 `mysql`, `python`의 컨테이너로 구성하였습니다.
```bash
# python package

mysql-connector-python==8.0.31
fastapi[all]==0.88.0
sqlalchemy==1.4.44
pymysql==1.0.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

pytest==7.2.0
pytest-cov==4.0.0
```
# run
```bash
$ cd app
> account_book/app
$ docker-compose up -d --build
```
`docker-compose.yml`이 있는 dir로 이동하여 `up`을 실행하면 작동합니다.  
`mysql:5.7`, `python:3.9` 이미지를 다운 받고 자동으로 실행합니다.
# test
```bash
$ pwd
> account_book/app/src/app/routers/api_v1/endpoints/tests_endpoint
```
위의 경로에 API에 대한 테스트 항목이 있습니다.
코드 커버리지는 90%입니다.  
![Code Coverage](test_coverage.png)

# API documents
http://localhost:8080/docs 로 이동하면 API swagger를 확인 할 수 있습니다.  

# ERD
![ERD](ERD.drawio.png)

데이터베이스는 간단하게 설계하였습니다.
한 user에 여러개의 receipt(영수증/가계부)를 가질 수 있고, 각 receipt에는 원래 하나의 detail이 있지만,  
detail은 복사가 가능하여 하나의 receipt에 여러개의 detail을 가질 수 있습니다.  
또한 각 detail은 하나의 link url을 가질 수 있습니다.  

# Tree
```bash
account_book
└─src
    └─app  <- root dir
    │   ├─models  <- DB models
    │   │  └─...
    │   ├─routers  <- APIs
    │   │  ├─api_v1  <- v1 APIs
    │   │  │  ├─endpoints  <- endpoints
    │   │  │  │  ├─tests_endpoint  <- tests
    │   │  │  │  │  └─...
    │   │  │  │  └─...
    │   │  │  └─...
    │   │  └─...
    │   ├─schemas  <- pydantic models
    │   │  └─...
    │   └─...  <- main, DB connect, config
    └─...  <- Dockerfile, compose, init-DB, requirements, wait-for-it    
```

# 요구사항 관련 APIs
1. 고객은 이메일과 비밀번호 입력을 통해서 회원 가입을 할 수 있습니다.  
    ```bash
   # 회원가입
   POST http://localhost:8080/api/v1/user/ 
   JSON {"email": <email>, "password": <password>}
   ```
2. 고객은 회원 가입이후, 로그인과 로그아웃을 할 수 있습니다.  
    ```bash
   # 로그인
   POST http://localhost:8080/api/v1/login/access-token/
   FORM {"username": <email>, "password": <password>}
   
   # 로그아웃
   로그아웃은 Frontend에서 access-token을 삭제하는 것이 성능적으로 우수하여 구현하지 않았습니다.
    ```
3. 고객은 로그인 이후 가계부 관련 아래의 행동을 할 수 있습니다. 
    1. 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.  
       ```bash 
       <<required Authorize>>
       # 가계부 생성
       POST http://localhost:8080/api/v1/receipt/
       JSON {
             "receipt_info": {"payment": <금액>, "store": <가게이름>, "memo": <메모>},
             "detail_info": {"payment_method": <결제방법>, "store_address": <가게주소>, "store_phone": <가게번호>, "store_info": <가게정보>}
       }  
       ```
    2. 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다.  
       ```bash
       <<required Authorize>>
       # 가계부 수정
       PUT http://localhost:8080/api/v1/receipt/<가계부ID>
       JSON {"payment": <금액수정>, "memo": <메모수정>}
       ```
    3. 가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다.  
       ```bash
       <<required Authorize>>
       # 가계부 삭제
       DELETE http://localhost:8080/api/v1/receipt/<가계부ID>
       ```
    4. 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다. 
       ```bash
       <<required Authorize>>
       # 가계부 리스트
       GET http://localhost:8080/api/v1/receipt/
       ```
    5. 가계부에서 상세한 세부 내역을 볼 수 있습니다. 
       ```bash
       <<required Authorize>>
       # 가계부 상세내역
       GET http://localhost:8080/api/v1/detail/<상세ID>
       ```
    6. 가계부의 세부 내역을 복제할 수 있습니다.
       ```bash
       <<required Authorize>>
       # 가계부 상세내역 복사
       POST http://localhost:8080/api/v1/detail/<상세ID>
       
       ```
    7. 가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
    (단축 URL은 특정 시간 뒤에 만료되어야 합니다.)
       ```bash
       <<required Authorize>>
       # 가계부 상세내역 공유 링크 생성
       POST http://localhost:8080/api/v1/link/
       JSON {"detail_id": <상세ID>, "ttl": <유효기간(일)>}
       ```
4. 로그인하지 않은 고객은 가계부 내역에 대한 접근 제한 처리가 되어야 합니다.
   ```bash
   JWT를 이용해서<<required Authorize>>가 있는 API는 token을 전달 해야 자원을 사용할 수 있습니다. 
   ```