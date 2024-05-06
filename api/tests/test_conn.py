from unittest.mock import patch
from queries.users import UsersRepo
from models import UserIn


def test_create_user_adds_to_database(database_connection):
    # Instantiate UsersRepo
    users_repo = UsersRepo()
    user_data = UserIn(
        email="test@example.com",
        username="testuser",
        name="Test User",
        password="password123"
    )

    # Create a user
    with patch("queries.users.pool", new=database_connection):
        created_user = users_repo.create_user(user_data)

    # Assert that the user is created successfully
    assert created_user is not None

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
