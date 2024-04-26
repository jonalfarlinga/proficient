from .pool import pool
from models import UserIn, UserOut


class UsersRepo:
    def create_user(self, user: UserIn) -> UserOut | None:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        INSERT INTO users
                            (email, username, name, password)
                        VALUES (%s, %s, %s, %s)
                        RETURNING
                            id, name, username, email
                        """,
                        (
                            user.email,
                            user.username,
                            user.name,
                            user.password
                        )
                    )
                    print(db)
                    id = db.fetchone()[0]
                    print()
                    print("id", id)
                    return UserOut(
                        id=id,
                        **user.dict()
                    )
        except Exception as e:
            print(":::::::::::::::::::::")
            print(e.pgresult)
            print(str(e), dir(e))
            print(":::::::::::::::::::::")
