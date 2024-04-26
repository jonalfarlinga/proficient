steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY NOT NULL,
            email VARCHAR(254) NOT NULL UNIQUE,
            username VARCHAR(100) NOT NULL UNIQUE,
            name VARCHAR(100) NOT NULL,
            password VARCHAR(255) NOT NULL UNIQUE
        )
        """,
        # "Down" SQL statement
        """
        DROP TABLE users;
        """
    ]
]
