# UFS Casting Agency
[![ci](https://github.com/bplusv/ufs-casting-agency/workflows/ci/badge.svg?branch=master)](https://github.com/bplusv/ufs-casting-agency/actions?query=workflow%3Aci+branch%3Amaster) [![codecov](https://codecov.io/gh/bplusv/ufs-casting-agency/branch/master/graph/badge.svg?token=77LGDR4ANN)](https://codecov.io/gh/bplusv/ufs-casting-agency)

UFS Casting Agency is an API to manage actors and movies data, including users authentication and permissions by user role.
- Back-end REST API built with Flask, SQLAlchemy and Postgresql.
- Authentication & Roles with Auth0 service + JWT (JSON Web Tokens).
- API Unit tests with pytest & SQLite.

## User Roles
- Casting Assistant can view actors and movies data.
- Casting Director can view actors and movies data, manage actors, and update existing movies.
- Executive Producer can view actors and movies data, manage actors, and manage movies.

## Getting Started

### Install Docker
You need to install the Docker runtime for your OS from [Get Docker](https://docs.docker.com/get-docker).

### Build & run servers
```
$ docker-compose up -d
```

The project includes a docker-compose.yml file, it will automatically download, build, and run the required docker images into containers. Your site will be accesible at 127.0.0.1:80.

The flask server and postgres containers will run, all the required libraries will be installed, and the Flask DB Migration will create all the required tables automatically.

### Run unit tests
```
$ docker exec ufs-casting-agency_webapp_1 pytest test
```
Unit tests use the pytest library. You can run the unit tests inside the container since pytest it's already installed, or you can install pytest locally and run the unit tests from your machine.

### Run linting
```
$ docker exec ufs-casting-agency_webapp_1 flake8 src test
```
This project follows the PEP8 Style Guide for python code. You can run flake8 linting inside the container since flake8 it's already installed, or you can install the flake8 locally and run the linter from your machine.

## API Documentation

### GET /api/actors
Returns data for all actors.

Request
```
$ curl -X GET -H "Authorization: Bearer $TOKEN" localhost/api/actors
```

Response
```
[
    {
        "id": 1,
        "name": "Joe Gainwell",
        "age": 23,        
        "gender": "male", 
        "movies": [
            1
        ]
    },
    {
        "id": 2,
        "name": "Michelle Ortega",
        "age": 19,
        "gender": "female",
        "movies": [
            2
        ]
    }
]
```

### GET /api/actors/<actor_id>
Returns data for the specified actor.
- actor_id is specified at the end of the url as an integer

Request
```
$ curl -X GET -H "Authorization: Bearer $TOKEN" localhost/api/actors/1
```

Response
```
{
  "id": 1,
  "name": "Joe Gainwell",
  "age": 23, 
  "gender": "male", 
  "movies": [
    1
  ]
}
```

### DELETE /api/actors/<actor_id>
Deletes the specified actor.
- actor_id is specified at the end of the url as an integer

Request
```
$ curl -X DELETE -H "Authorization: Bearer $TOKEN" localhost/api/actors/1
```

Response
```
{
  "success": true
}
```

### POST /api/actors
Adds a new actor with the specified data.
- movies id list is optional

Request
```
$ curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"name": "Joe Gainwell", "age": 23, "gender": "male", "movies": [1]}' localhost/api/actors
```

Response
```
{
  "actor_id": 1,
  "success": true
}
```

### PATCH /api/actors/<actor_id>
Updates data for the specified actor.
- actor_id is specified at the end of the url as an integer
- all fields are optional

Request
```
$ curl -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"name": "Joe J Gainwell", "movies": [2]}' localhost/api/actors/1
```

Response
```
{
  "success": true
}
```

### GET /api/movies
Returns data for all movies

Request
```
$ curl -X GET -H "Authorization: Bearer $TOKEN" localhost/api/movies
```

Response
```
[
  {
    "id": 1,
    "title": "Back to the future 4",
    "release_date": "Thu, 01 Apr 2021 00:00:00 GMT",
    "actors": [
      1
    ]
  },
  {
    "id": 2,
    "title": "A new bright sunshine",
    "release_date": "Thu, 01 Sep 2022 00:00:00 GMT",
    "actors": [
      2
    ]
  }
]
```

### GET /api/movies/<movie_id>
Returns data for the specified movie.
- movie_id is specified at the end of the url as an integer

Request
```
$ curl -X GET -H "Authorization: Bearer $TOKEN" localhost/api/movies/1
```

Response
```
{
  "id": 1,
  "title": "Back to the future 4",
  "release_date": "Thu, 01 Apr 2021 00:00:00 GMT",
  "actors": [
    1
  ]
}
```

### DELETE /api/movies/<movie_id>
Deletes the specified movie.
- movie_id is specified at the end of the url as an integer

Request
```
$ curl -X DELETE -H "Authorization: Bearer $TOKEN" localhost/api/movies/1
```

Response
```
{
  "success": true
}
```

### POST /api/movies
Adds a new movie with the specified data.
- actors id list is optional

Request
```
$ curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"title": "Back to the future 4", "release_date": "2021-04-01", "actors": [1]}' localhost/api/movies
```

Response
```
{
  "movie_id": 1,
  "success": true
}
```

### PATCH /api/movies/<movie_id>
Updates data for the specified movie.
- movie_id is specified at the end of the url as an integer
- all fields are optional

Request
```
$ curl -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"release_date": "2021-04-01", "actors": [1]}' localhost/api/movies/1
```

Response
```
{
  "success": true
}
```

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": false, 
    "error": 400,
    "message": "bad request"
}
```
The API will return the following error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Entity Not Found
- 422: Unprocessable Entity
- 500: Internal Server Error

## Authors
[Luis Salazar](https://github.com/bplusv)
