from psycopg_pool import ConnectionPool
import os
pool = ConnectionPool(open=True, conninfo=os.environ["DATABASE_URL"])
