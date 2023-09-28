# 근태관리 프로그램

로그인 기록 작성 및 일별기록 확인가능한 RESTAPI 제공

## 실행방법

```Bash
# dev
docker-compose up -d

# product
docker-compose -f docker-compose.prod.yaml up --build
```

## 시스템 구성

- Backend : Django (Django Rest Framework)  + Nginx + Gunicorn + Docker
- DB : PostgreSQL
- Infra : Docker

## 사용 기술

- Django Rest Framework
- Django + Nginx + Gunicorn + Docker
- dj-rest-auth : REST API를 통한 로그인/로그아웃 제공

## 데이터베이스 설계

[record ERD](https://www.erdcloud.com/d/RACtxBeL3C63ePSM8)

## API 설계

| INDEX | METHOD | URL                    | DESCRIPTION             |
| ----- | ------ | ---------------------- | ----------------------- |
| 1     | GET    | /access                | 로그인 기록 리스트 조회 |
| 2     | POST   | /access                | 로그인 기록 작성        |
| 3     | GET    | /access/{id}           | ID별 로그인 기록 조회   |
| 4     | PUT    | /access/{id}           | ID별 로그인 기록 수정   |
| 5     | DELETE | /access/{id}           | ID별 로그인 기록 삭제   |
| 6     | GET    | /access/user/{user_id} | 유저별 로그인 기록 조회 |
| 7     | GET    | /daily                 | 일별기록 리스트 조회    |
| 8     | POST   | /daily                 | 일별기록 작성           |
| 9     | GET    | /daily/{id}            | ID별 일별기록 조회      |
| 10    | PUT    | /daily/{id}            | ID별 일별기록 수정      |
| 11    | DELETE | /daily/{id}            | ID별 일별기록 삭제      |
| 12    | GET    | /daily/user/{user_id}  | 유저별 일별기록 조회    |

## 주요 업데이트

### 1. Nginx + Gunicorn + Django + Docker

- Nginx + Gunicorn + Django + Docker 환경 구성

- 참고 사이트
  1. [[실전] Docker + Nginx + gunicorn + django](https://velog.io/@masterkorea01/Docker-Nginx-gunicorn-django)
  2. [웹서비스의 구성 - Web Server , CGI, WAS , WSGI의 특징 및 차이점](https://my-repo.tistory.com/20?category=918048)

### 2. Swagger 적용

- Django REST Swagger(drf_yasg module)을 적용하여 API 문서 생성
- Swagger 에서 POST 실행 시 csrf token 에러가 발생하는데 Responses Curl 부분과 쿠키를 맞춰주면 해결된다.

### 3. Test Code 적용

### - 테스트 종류

1. unit test(유닛테스트)
   - 독립적인 class와 function 단위의 테스트
2. Regression test(버그 수정 테스트)
   - 발생하였던 버그에 대한 수정 테스트
3. Integration test(통합테스트)
   - 유닛 테스크를 완료한 각각의 독립적인 컴포넌트들이 함께 결합하여 수행하는 동작을 검증.
   - 각 컴포넌트들의 내부적인 동작까지는 검증할 필요가 없다. 해석해보면 비즈니스 로직에 대한 검증인거 같다

### - 테스트 함수

```python
self.assertEquals # 생각한 값과 같은지 체크해주는 함수
self.assertTrue(True) # () 안의 값이 True인지 체크
self.assertFalse(False) # () 안의 값이 False인지 체크
```

### - Test Setting

Test용 DB가 따로 생성되기 때문에 superuser 등 기본 세팅을 해줘야한다.

- 참고 사이트 : https://docs.djangoproject.com/en/4.1/topics/testing/overview/

### - Django Rest Framework의 Testing

APIRequestFactory를 통해 CRUD 테스트를 짧은 코드로도 만들 수 있다.

- 참고 사이트 : https://www.django-rest-framework.org/api-guide/testing/

### 4. 유효성 검사 (validators)

- AccessRecord 모델의 tag는 IN, OUT만 가능하도록 제한이 필요하다고 느꼈음
- 모델에 validators 인수를 추가하면 가능하다. 처음엔 안되서 찾아보니 Django Rest Framework에서는 serializers.py에 추가해야한다는 설명이 있는데 모델에 추가해야 동작했다.
- 참고 사이트 : https://docs.djangoproject.com/en/4.1/ref/validators/

### 5. MultipleValueDictKeyError 수정

```python
data["check_time"] # 데이터가 존재하지 않을 경우 MultipleValueDictKeyError
data.get("check_time", False) # 데이터가 없으면 False로 처리
```
