# Casting-Agency-API

The Casting Agency models a company that is responsible for creating movies, and managing and assigning actors to those movies in order to simplify and streamline the processes within the company.

The Casting Agency API allows for:

1. Displaying actors.
2. Displaying movies.
3. Adding, updating and deleting actors.
4. Adding, updating and deleting movies.
5. Adding actors to movies.
6. Removing actors from movies.


## Hosted Application

The application is deployed to Heroku at: https://mg-casting-agency.herokuapp.com/

## Roles and Permissions

There are 3 different roles defined for accessing the Casting Agency API:
1. Casting Assistant
2. Casting Director
3. Executive Producer

<br/>

**Permissions**   | **Casting Assistant**  | **Casting Director**   | **Executive Producer** |
------------- | -----------------  | ------------------ | ------------------ |
get:actors    | :white_check_mark: | :white_check_mark: | :white_check_mark: |
post:actors   |                    | :white_check_mark: | :white_check_mark: |
patch:actors  |                    | :white_check_mark: | :white_check_mark: |
delete:actors |                    | :white_check_mark: | :white_check_mark: |
get:movies    | :white_check_mark: | :white_check_mark: | :white_check_mark: |
post:movies   |                    |                    | :white_check_mark: |
patch:movies  |                    | :white_check_mark: | :white_check_mark: |
delete:movies |                    |                    | :white_check_mark: |

<br/>

## Setting up authentication

To request any of the API endpoints described below, you must authenticate your requests using a `Bearer` token in the headers of the request.

For testing purposes, you can login with the following username and password combinations:
1. `Casting Assistant`
    - login: `joe@casting-agency.com`
    - password: `abcd1234!@$`
2. `Casting Director`
    - login: `ann@casting-agency.com`
    - password: `abcd1234!@$`
3. `Executive Producer`
    - login: `adam@casting-agency.com`
    - password: `abcd1234!@$`

You can login using the following URL, and get the required access token from the authenticated URL:

`https://fsnd-casting-agency.eu.auth0.com/authorize?audience=agency&response_type=token&client_id=l5buZVd3KWO4wghf7S5RvHZqZZtoU0hy&redirect_uri=http://127.0.0.1:5000`


## Setup for Local Development

### Tech Stack

The tech stack includes the following:

* **SQLAlchemy ORM** - the ORM library
* **PostgreSQL** - the database
* **Python3** and **Flask** - the server language and server framework
* **Flask-Migrate** - for creating and running schema migrations

### Installing Dependencies

#### Python 3

Follow instructions to install the latest version of Python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PostgreSQL

Follow instructions to install the latest version of [PostgreSQL](https://www.postgresql.org/download/) for your platform

#### Virtual Environment

It is recommended to work within a virtual environment. This keeps the dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

If you are using Python 3.3 or newer, the `venv` module is the preferred way to create and manage virtual environments. `venv` is included in the Python standard library and requires no additional installation.
To create a virtual environment using `venv`, navigate to the root directory (`Casting-Agency-API`) and run:
```bash
python3 -m venv venv
. venv/bin/activate
```
The `venv` folder should be added to `.gitignore`.

#### PIP Dependencies

Install dependencies by navigating to the root directory (`Casting-Agency-API`) and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

### Running the server locally
To run the server, execute from within the root directory (`Casting-Agency-API`):

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

### Database Local Setup
With PostgreSQL running, restore a database using the `agency.psql` file provided. From the root directory (`Casting-Agency-API`) in the Terminal run:
```bash
dropdb --if-exists agency
createdb agency
psql agency < agency.psql
```

## Testing locally
To run the tests, execute from within the root directory (`Casting-Agency-API`):
```
dropdb --if-exists agency_test
createdb agency_test
psql agency_test < agency.psql
python test_app.py
```
The `HtmlTestRunner` package is used to generate human-readable HTML test reports showing the results of the tests of the Casting Agency API. 
The HTML test reports from different test runs can be found in the `test-results` directory.

## Casting Agency API Reference

<br/>

| **Resource URL**         | **Method** | **Description**                      | **Permission** |
| ------------------------ | ---------- | ------------------------------------ | -------------  |
| /                        | GET        | Default route - it returns the string “This is the Casting Agency API” | public endpoint |
| /actors                  | GET        | Return all actors                    | get:actors     |
| /actors                  | POST       | Add a new actor                      | post:actors    |
| /actors/`<int:actor_id>` | PATCH      | Update an actor                      | patch:actors   |
| /actors/`<int:actor_id>` | DELETE     | Delete an actor                      | delete:actors  |
| /movies                  | GET        | Return all movies                    | get:movies     |
| /movies                  | POST       | Add a new movie                      | post:movies    |
| /movies/`<int:movie_id>` | PATCH      | Update a movie                       | patch:movies   |
| /movies/`<int:movie_id>` | DELETE     | Delete a movie                       | delete:movies  |
| /movies/`<int:movie_id>`/actors | POST | Add an actor to a movie             | post:movies    |
| /movies/`<int:movie_id>`/actors/`<int:actor_id>` | DELETE | Delete an actor from a movie | delete:movies |


## Endpoints

### GET /
- Default route - it returns the string “This is the Casting Agency API”
- It is a public endpoint
- Request arguments: None

**Testing using cURL**
- Request: `curl https://mg-casting-agency.herokuapp.com/`
- Response (200 OK):
```
This is the Casting Agency API
```

### GET /actors
- Return all actors
- It requires the `get:actors` permission
- Request arguments: None

**Testing using cURL**
- Export the token for the Casting Assistant: `export TOKEN='bearer token goes here'`
- Request: `curl -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" https://mg-casting-agency.herokuapp.com/actors`
- Response (200 OK):
```
{
  "actors": [
    {
      "age": 35, 
      "gender": "female", 
      "id": 1, 
      "movies": [
        {
          "genre": "Thriller", 
          "release_year": "2011", 
          "title": "The Girl with the Dragon Tattoo"
        }
      ], 
      "name": "Rooney Mara"
    }, 
    {
      "age": 62, 
      "gender": "male", 
      "id": 2, 
      "movies": [
        {
          "genre": "Drama", 
          "release_year": "1994", 
          "title": "The Shawshank Redemption"
        }
      ], 
      "name": "Tim Robbins"
    }, 
    {
      "age": 28, 
      "gender": "male", 
      "id": 3, 
      "movies": [
        {
          "genre": "Thriller", 
          "release_year": "2008", 
          "title": "The Dark Knight"
        }
      ], 
      "name": "Heath Ledger"
    }
  ], 
  "success": true
}
```

### POST /actors
- Add a new actor
- It requires the `post:actors` permission
- Request arguments: None

**Testing using cURL**
- Export the token for the Casting Director: `export TOKEN='bearer token goes here'`
- Request: `curl -X POST https://mg-casting-agency.herokuapp.com/actors -H "Content-Type: application/json" -H "Accept: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"name":"Joaquin Phoenix", "age":46, "gender":"male"}'`
- Response (200 OK):
```
{
  "actor": {
    "age": 46, 
    "gender": "male", 
    "id": 23, 
    "movies": [], 
    "name": "Joaquin Phoenix"
  }, 
  "success": true
}
```

### PATCH /actors/`<int:actor_id>`
- Update an actor with a given ID if the ID exists
- It requires the `patch:actors` permission
- Request arguments: `actor_id` (integer, mandatory)

**Testing using cURL**
- Export the token for the Casting Director: `export TOKEN='bearer token goes here'`
- Request: `curl -X PATCH https://mg-casting-agency.herokuapp.com/actors/2 -H "Content-Type: application/json" -H "Accept: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"name":"Harrison Ford", "age":78, "gender":"male", "movie_id":4}'`
- Response (200 OK):
```
{
  "actor": {
    "age": 78, 
    "gender": "male", 
    "id": 2, 
    "movies": [
      {
        "genre": "Drama", 
        "release_year": "1994", 
        "title": "The Shawshank Redemption"
      }
    ], 
    "name": "Harrison Ford"
  }, 
  "success": true
}
```

### DELETE /actors/`<int:actor_id>`
- Delete an actor with a given ID if the ID exists
- It requires the `delete:actors` permission
- Request arguments: `actor_id` (integer, mandatory)

**Testing using cURL**
- Export the token for the Casting Director: `export TOKEN='bearer token goes here'`
- Request: `curl -X DELETE https://mg-casting-agency.herokuapp.com/actors/23 -H "Content-Type: application/json" -H "Accept: application/json" -H "Authorization: Bearer ${TOKEN}"`
- Response (200 OK):
```
{
  "actor_id": 23, 
  "success": true
}
```

### GET /movies
- Return all movies
- It requires the `get:movies` permission
- Request arguments: None

**Testing using cURL**
- Export the token for the Casting Assistant: `export TOKEN='bearer token goes here'`
- Request: `curl -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" https://mg-casting-agency.herokuapp.com/movies`
- Response (200 OK):
```
{
  "movies": [
    {
      "actors": [
        {
          "age": 82, 
          "gender": "male", 
          "name": "Morgan Freeman"
        }, 
        {
          "age": 78, 
          "gender": "male", 
          "name": "Harrison Ford"
        }
      ], 
      "genre": "Drama", 
      "id": 1, 
      "release_year": "1994", 
      "title": "The Shawshank Redemption"
    }, 
    {
      "actors": [], 
      "genre": "Drama", 
      "id": 2, 
      "release_year": "1972", 
      "title": "The Godfather"
    }, 
    {
      "actors": [
        {
          "age": 28, 
          "gender": "male", 
          "name": "Heath Ledger"
        }, 
        {
          "age": 82, 
          "gender": "male", 
          "name": "Morgan Freeman"
        }
      ], 
      "genre": "Thriller", 
      "id": 3, 
      "release_year": "2008", 
      "title": "The Dark Knight"
    }
  ], 
  "success": true
}

```

### POST /movies/
- Add a new movie
- It requires the `post:movies` permission
- Request arguments: None

**Testing using cURL**
- Export the token for the Executive Producer: `export TOKEN='bearer token goes here'`
- Request: `curl -X POST https://mg-casting-agency.herokuapp.com/movies -H "Content-Type: application/json" -H "Accept: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"title":"The Fugitive", "release_year":"1993", "genre":"Action"}'`
- Response (200 OK):
```
{
  "movie": {
    "actors": [], 
    "genre": "Action", 
    "id": 34, 
    "release_year": "1993", 
    "title": "The Fugitive"
  }, 
  "success": true
}
```

### PATCH /movies/`<int:movie_id>`
- Update a movie with a given ID if the ID exists
- It requires the `patch:movies` permission
- Request arguments: `movie_id` (integer, mandatory)

**Testing using cURL**
- Export the token for the Casting Director: `export TOKEN='bearer token goes here'`
- Request: `curl -X PATCH https://mg-casting-agency.herokuapp.com/movies/10 -H "Content-Type: application/json" -H "Accept: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"title":"Blade Runer", "release_year":"1982", "genre":"Sci-Fi"}'`
- Response (200 OK):
```
{
  "movie": {
    "actors": [
      {
        "age": 56, 
        "gender": "male", 
        "name": "Brad Pitt"
      }
    ], 
    "genre": "Sci-Fi", 
    "id": 10, 
    "release_year": "1982", 
    "title": "Blade Runer"
  }, 
  "success": true
}
```

### DELETE /movies/`<int:movie_id>`
- Delete a movie with a given ID if the ID exists
- It requires the `delete:movies` permission
- Request arguments: `movie_id` (integer, mandatory)

**Testing using cURL**
- Export the token for the Executive Producer: `export TOKEN='bearer token goes here'`
- Request: `curl -X DELETE https://mg-casting-agency.herokuapp.com/movies/33 -H "Content-Type: application/json" -H "Accept: application/json" -H "Authorization: Bearer ${TOKEN}"`
- Response (200 OK):
```
{
  "movie_id": 33, 
  "success": true
}
```

### POST /movies/`<int:movie_id>`/actors
- Add an actor to a movie
- It requires the `post:movies` permission
- Request arguments: `movie_id` (integer, mandatory)

**Testing using cURL**
- Export the token for the Executive Producer: `export TOKEN='bearer token goes here'`
- Request: `curl -X POST https://mg-casting-agency.herokuapp.com/movies/8/actors -H "Content-Type: application/json" -H "Accept: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"actor_id":15}'`
- Response (200 OK):
```
{
  "movie": {
    "actors": [
      {
        "age": 55, 
        "gender": "female", 
        "name": "Viola Davis"
      }
    ], 
    "genre": "Drama", 
    "id": 8, 
    "release_year": "2011", 
    "title": "The Help"
  }, 
  "success": true
}
```

### DELETE /movies/`<int:movie_id>`/actors/`<int:actor_id>`
- Delete an actor from a movie
- It requires the `delete:movies` permission
- Request arguments: `movie_id` (integer, mandatory), `actor_id` (integer, mandatory)
 
**Testing using cURL**
- Export the token for the Executive Producer: `export TOKEN='bearer token goes here'`
- Request: `curl -X DELETE https://mg-casting-agency.herokuapp.com/movies/8/actors/15 -H "Content-Type: application/json" -H "Accept: application/json" -H "Authorization: Bearer ${TOKEN}"`
- Response (200 OK):
```
{
  "actor_id": 15, 
  "movie_id": 8, 
  "success": true
}
```

<br/>

### Error Handling
Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return the following error types when requests fail: 
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 409: Conflict
- 422: Unprocessable Request