from unittest.mock import patch
from queries.users import UsersRepo
from models import DatabaseError, UserIn, UserOut, UserOutWithPassword


def test_create_new_user(database_connection):
    # Instantiate UsersRepo
    users_repo = UsersRepo()
    user_data = UserIn(
        email="test@example.com",
        username="testuser",
        name="Test User",
        password="password"
    )

    # Create a user
    with patch("queries.users.pool", new=database_connection):
        created_user = users_repo.create_user(user_data)

    # Assert that the user is created successfully
    assert isinstance(created_user, UserOut)

    # Fetch the user from the database
    with database_connection.connection() as conn:
        with conn.cursor() as db:
            db.execute(
                """
                SELECT * FROM users
                WHERE id = %s
                """,
                (created_user.id,)
            )
            fetched_users = db.fetchall()

    for row in fetched_users:
        if row[0] == created_user.id:
            fetched_user = row

    # Assert that the user is in the database and its details match
    assert fetched_users is not None
    assert fetched_user[0] == created_user.id
    assert fetched_user[1] == user_data.email
    assert fetched_user[2] == user_data.username
    assert fetched_user[3] == user_data.name


def test_create_user_with_same_name(database_connection):
    # Instantiate UsersRepo
    users_repo = UsersRepo()
    user_data = UserIn(
        email="test2@example.com",
        username="testuser2",
        name="Test User",
        password="password1"
    )

    # Create a user
    with patch("queries.users.pool", new=database_connection):
        created_user = users_repo.create_user(user_data)

    # Assert that the user is created successfully
    assert isinstance(created_user, UserOut)

    # Fetch the user from the database
    with database_connection.connection() as conn:
        with conn.cursor() as db:
            db.execute(
                """
                SELECT * FROM users
                WHERE id = %s
                """,
                (created_user.id,)
            )
            fetched_users = db.fetchall()

    for row in fetched_users:
        if row[0] == created_user.id:
            fetched_user = row

    # Assert that the user is in the database and its details match
    assert fetched_users is not None
    assert fetched_user[0] == created_user.id
    assert fetched_user[1] == user_data.email
    assert fetched_user[2] == user_data.username
    assert fetched_user[3] == user_data.name


def test_create_duplicate_email(database_connection):
    # Instantiate UsersRepo
    users_repo = UsersRepo()
    user_data = UserIn(
        email="test@example.com",
        username="testuser3",
        name="Test User 3",
        password="password12"
    )

    # Create a user
    with patch("queries.users.pool", new=database_connection):
        created_user = users_repo.create_user(user_data)

    # Assert that the user is created successfully
    assert isinstance(created_user, DatabaseError)
    assert created_user.failure == "Failed to insert user"
    assert "Key (email)" in created_user.detail


def test_create_duplicate_username(database_connection):
    # Instantiate UsersRepo
    users_repo = UsersRepo()
    user_data = UserIn(
        email="test4@example.com",
        username="testuser",
        name="Test User 4",
        password="password123"
    )

    # Create a user
    with patch("queries.users.pool", new=database_connection):
        created_user = users_repo.create_user(user_data)

    # Assert that the user is created successfully
    assert isinstance(created_user, DatabaseError)
    assert created_user.failure == "Failed to insert user"
    assert "Key (username)" in created_user.detail


def test_get_users(database_connection):
    # Arrange
    repo = UsersRepo()

    # Act
    with patch("queries.users.pool", new=database_connection):
        users = repo.get_user()

    # Assert
    assert isinstance(users, list)
    assert len(users) == 2

    for user in users:
        assert isinstance(user, UserOut)
        assert user.name == "Test User"
        assert not hasattr(user, "password")


def test_get_a_user(database_connection):
    # Arrange
    repo = UsersRepo()

    # Act
    with patch("queries.users.pool", new=database_connection):
        fetched_user = repo.get_user('testuser')

    # Assert that the user is in the database and its details match
    assert isinstance(fetched_user, UserOut)
    assert fetched_user.email == "test@example.com"
    assert fetched_user.username == "testuser"
    assert fetched_user.name == "Test User"
    assert not hasattr(fetched_user, "password")


def test_get_no_user(database_connection):
    # Arrange
    repo = UsersRepo()

    # Act
    with patch("queries.users.pool", new=database_connection):
        fetched_user = repo.get_user('nouser')

    # Assert
    assert fetched_user is None


def test_get_user_with_password(database_connection):
    # Arrange
    repo = UsersRepo()

    # Act
    with patch("queries.users.pool", new=database_connection):
        fetched_user = repo.get_user_with_password('testuser')

    # Assert that the user is in the database and its details match
    assert isinstance(fetched_user, UserOutWithPassword)
    assert fetched_user.email == "test@example.com"
    assert fetched_user.username == "testuser"
    assert fetched_user.name == "Test User"
    assert fetched_user.password == "password"


def test_get_no_user_with_password(database_connection):
    # Arrange
    repo = UsersRepo()

    # Act
    with patch("queries.users.pool", new=database_connection):
        fetched_user = repo.get_user_with_password('nouser')

    # Assert
    assert fetched_user is None
