# PROFicient
This app is a portal to a set of university-teaching focused utilities

### CONTENTS

- [Welcome](#welcome)
  - [Getting Started](#getting-started)
- [Documentation](#documentation)
  - [Development](#development)
  - [Data Repositories](#data-repository)
    - [Users Repo](#users-repo)

## Welcome!

<img src="./docs/proficient_screenshot.png" width="500" align="center">

### Getting Started

To get The Proficient Professor working for you, navigate to the [home page](https://www.proficientdr.com). If this is your first time, click on "Create an Account". On the sign up page, enter your username, email, and password. The click on "Sign up". This will log you in, and share your session with the Proficient apps (I haven't implemented logged in features yet on the other apps).

From the Dashboard, you can review the whole Proficient app family, and jump to one with a button click.

A logged in user has access to the Profile page. On this page, you can update your user information by clicking "Edit" next to one or more fields, then clicking "Update". 

## Documentation

### Development

- I wrote this app in JavaScript and Python, using VSCode.
- The Backend API is built on FastAPI running on a uvicorn server.
- The Front End is a single-page-app built with Vite-React.
- The dev environment runs in Docker and the repo is hosted on Github.

<p align="center">
<img src="./docs/vscode_icon.png" width="40"></img>
<img src="./docs/javascript_icon.png" width="40"></img>
<img src="./docs/python_icon.png" width="40"></img>
<img src="./docs/react_icon.png" width="40"></img>
<img src="./docs/fastapi.svg" width="40"></img>
<img src="./docs/docker_icon.png" width="40"></img>
</p>

**Local deployment**

The repository is built to run using Docker compose. Sensitive environment variables such as SIGNING_KEY are hard-coded in the `docker-compose.yaml` because it is only used in the dev environment. The live app will use individual containers with secure environment variables.

1. Create a volume called prof-db
    - `docker volume create prof-db`
2. Build the docker image using docker compose
    - `docker-compose build` in the repository directory
3. Run the docker compose container
    - `docker-compose run` in the repository directory

The backend runs on `localhost:5200` and the frontend on `localhost:5300`

**Backend Test Environment**

There is also an environment designed for lightweight backend testing.

1. Build a docker image from the `/api` directory
    - `docker build . -f Dockerfile.test -t proficient-pytest`
2. Run the docker container from the `/api` directory
    - `docker run -v "$(pwd):/app" --name proficient-pytest-1 proficient-pytest`
3. Connect to the container bash
    - `docker exec -it proficient-pytest-1 bash`
4. Run pytest from the bash root directory
    - `python -m pytest tests`

With this process, the backend api can be tested without creating a volume. The database is mocked using an in-memory db provided by [testing.postgresql](https://github.com/tk0miya/testing.postgresql?tab=readme-ov-file#readme).

### Data Repository

Data for PROFicient is stored in a PostgreSQL database. The central entity for the app is the `users` table. PROFicient manages the user status and saved data for the PROFicient extensions, such as Calends.

### Users Repo

The `UsersRepo` class handles a connection to the PostgreSQL `users` table.

`class queries.users.UsersRepo`

UsersRepo depends on `queries.pool` and requires a valid `DATABASE_URL`
environmental variable.

- create_user

  Create a new user in the database.

  `create_user(user)`

  EXAMPLE
  ```python
  data = UserIn(
      username="string",
      email="string"
      name="string"
      password="string"
  )
  repo = UsersRepo()
  repo.create_user(data)
  ```

  Returns:

  ```python
  UserOut(
      username="string",
      name="string",
      email="string",
      password="string"
  )
  ```

- get_user

  Retrieve details about a user entry or a list of all users.

  `get_user(email=None)`

  EXAMPLE
  ```python
  user_email = "email"
  repo = UsersRepo()
  repo.get_user(user_email)
  ```

  Returns:
  ```python
  UserOut(
      id=int,
      username="string",
      name="string",
      email="string",
  )
  ```

  If email is `None`, the function returns a list of all entried in the `users` table as UserOut objects.

  If email is set, the function returns a single UserOut object.
  If email is set, but no user is found, the function returns None.

- get_user_with_password

  Retrieve details about a user, including the stored hashed password.

  **WARNING** This function should never be exposed to a user or external app. It is strictly for internal use.

  `get_user_with_password(user)`

  EXAMPLE
  ```
  user_email = "email"
  repo = UsersRepo()
  repo.get_user(user_email)
  ```

  Returns:

  ```python
  UserOut(
      id=int
      username="string",
      name="string",
      email="string",
      password="string"
  )
  ```
