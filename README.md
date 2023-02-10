# FastApi Starter Template

## Project Description

    Fast api starter template is a project you can use to start your project immediately. 
    It has all basic feature to start your project.Like 
        1. Authentication
        2. Database migrations
        3. Custom Response Middleware
        4. Custom Pagination 
        5. Dynamic Filter
        6. How to authenticate api
        7. Separate endpoint for public & private api.
        8. How to use redis & celery
        9. Seeder to generate initial data
        10. And Many More.

## To Run This Project

 python3 -m venv ./venv
 source venv/bin/activate
 pip install -r requirements.txt
 bash src/scripts/prestart.sh -> only for first time
    uvicorn src.main:app --reload -> it will run the project in <http://127.0.0.1:8000/>

## To Run Migration

    1. alembic revision — autogenerate -m "Your message" -> to generate migrations file.
    2. alembic upgrade head -> to apply the migrations

## Technology Used

    1. FastApi
    2. Alembic
    3. SQLModel Orm
    4. Redis
    5. Celery

## Api Documentation

    http://127.0.0.1:8000/docs

## Author

    Mahmudul Hassan
    mahmudul.hassan240@gmail.com
