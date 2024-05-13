# PROFicient
This app is a portal to a set of university-teaching focused utilities

### CONTENTS

- [Documentation](#documentation)
  - [Data Repositories](#data-repositories)
    - [Users Repo](#users-repo)

## Documentation

### Data Repositories

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
