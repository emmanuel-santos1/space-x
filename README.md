# Space-X-Fastapi
App using fastapi

## Technology Stack:
* FastAPI
* Uvicorn (server)
* Pytest
* Sqlalchemy
* Postgres
* Docker


## How to start the app ?
```
git clone git@github.com:emmanuel-santos1/space-x.git
cd .\space-x\
mkvirtualenv -p python3.10 -a space-x space-x  #create a virtual environment
pip install -r .\requirements.txt
cp .env-template .env
complete all environmet vars in .env file
docker build .
docker-compose build app
docker-compose up app
visit  127.0.0.1:8000/
Go to doc for more information
```

## How to run tests ?
```
pytest
```

## How to create new user ?
```
visit  127.0.0.1:8000/register/
Complete form
```

Features:
 - ✔️ Serving Template
 - ✔️ Schemas
 - ✔️ Dependency Injection
 - ✔️ Password Hashing
 - ✔️ Unit Testing (What makes an app stable)
 - ✔️ Authentication login/create user/get token
 - ✔️ Authorization/Permissions
 - ✔️ Logging
 - ✔️ Throttling
