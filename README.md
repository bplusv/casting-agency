# UFS Casting Agency

![ci](https://github.com/bplusv/ufs-casting-agency/workflows/ci/badge.svg?branch=master)

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
Unit tests use the pytest library. You can run the unit tests inside the container since pytest it's already installed, or you can install it locally and run the unit tests from your machine.

### Run linting

```
$ docker exec ufs-casting-agency_webapp_1 flake8 src test
```
This project follows the PEP8 Style Guide for python code. You can run flake8 linting inside the container since flake8 it's already installed, or you can install the flake8 library locally and run linting from your machine.
