from .pool import pool
from models import DatabaseError, UserIn, UserOut
import logging

logger = logging.getLogger(__name__)


class UsersRepo:
    def create_user(self, user: UserIn) -> UserOut | None:
        print(user)
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
                    id = db.fetchone()[0]
                    return UserOut(
                        id=id,
                        **user.dict()
                    )
        except Exception as e:
            logger.info(":::::::::::::::::::::")
            logger.info(e.pgresult)
            logger.info(str(e))
            logger.info(":::::::::::::::::::::")
            return DatabaseError(
                failure="Failed to insert user",
                detail=str(e)
            )

    def get_password(self, username: str) -> str:
        logger.debug(username)
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        SELECT password
                        FROM users
                        WHERE username = %s
                        """,
                        [username]
                    )
                    password = db.fetchone()[0]
                    return password
        except Exception as e:
            logger.info(":::::::::::::::::::::")
            logger.info(str(e))
            logger.info(":::::::::::::::::::::")
            return DatabaseError(
                failure="Failed to retrieve password",
                detail=str(e)
            )

    def get_user(self, username: str):
        logger.debug(username)
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        SELECT *
                        FROM users
                        WHERE username = %s
                        """,
                        [username]
                    )
                    user = db.fetchone()
                    user_out = UserOut(
                        id=user[0],
                        email=user[1],
                        username=user[2],
                        name=user[3],
                        password=user[4]
                    )
                    return user_out
        except Exception as e:
            logger.info(":::::::::::::::::::::")
            logger.info(str(e))
            logger.info(":::::::::::::::::::::")
            return DatabaseError(
                failure="Failed to retrieve user",
                detail=str(e)
            )
