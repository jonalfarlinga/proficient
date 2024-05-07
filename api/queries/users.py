from .pool import pool
from models import DatabaseError, UserIn, UserOut, UserOutWithPassword
import logging

logger = logging.getLogger(__name__)


class UsersRepo:
    def create_user(self, user: UserIn) -> UserOut | None:
        logger.debug(f'Create with data: "{str(user)}"')
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
                        **user.model_dump()
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

    def get_user_with_password(self, email: str) -> UserOutWithPassword:
        logger.debug(f'Get login data from: "{email}"')
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        SELECT *
                        FROM users
                        WHERE email = %s
                        """,
                        [email]
                    )
                    user = db.fetchone()
                    if not user:
                        return None
                    return UserOutWithPassword(
                        id=user[0],
                        email=user[1],
                        username=user[2],
                        name=user[3],
                        password=user[4]
                    )
        except Exception as e:
            logger.info(":::::::::::::::::::::")
            logger.info(str(e))
            logger.info(":::::::::::::::::::::")
            return DatabaseError(
                failure="Failed to retrieve password",
                detail=str(e)
            )

    def get_user(self, email: str = None):
        logger.debug(f'Get user data from: "{email}"')
        sql = ""
        query_data = []
        if email is not None:
            sql = "WHERE email = %s"
            query_data.append(email)
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        SELECT *
                        FROM users
                        """ + sql,
                        query_data
                    )
                    if email is not None:
                        user = db.fetchone()
                        if not user:
                            return None
                        user_out = UserOut(
                            id=user[0],
                            email=user[1],
                            username=user[2],
                            name=user[3],
                        )
                        return user_out
                    else:
                        users = db.fetchall()
                        user_data = []
                        for user in users:
                            user_data.append(
                                UserOut(
                                    id=user[0],
                                    email=user[1],
                                    username=user[2],
                                    name=user[3],
                                )
                            )
                        return user_data
        except Exception as e:
            logger.info(":::::::::::::::::::::")
            logger.info(str(e))
            logger.info(":::::::::::::::::::::")
            return DatabaseError(
                failure="Failed to retrieve user",
                detail=str(e)
            )
