import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from configuration.classType import GoogleUser
from configuration.config import URL_DATABASE 

# conn = None
# cur = None
# create_script = '''CREATE TABLE IF NOT EXISTS users (
#             id SERIAL PRIMARY KEY,
#             gid varchar(40) UNIQUE NOT NULL,
#             email varchar(255),
#             username varchar(100))'''
# existing_table = '''SELECT EXISTS (
#     SELECT 1
#     FROM information_schema.tables 
#     WHERE table_schema = 'public' -- ou un autre schéma
#     AND table_name = %s
# )
# '''

# # Définir les informations de connexion dans une variable de configuration
# DB_CONFIG = {
#     "host": "localhost",
#     "database": "tictactoe",
#     "user": "postgres",
#     "password": "relou123",
#     "port": "5432"
# }

URL_DATABASE_POSTGRESQL = URL_DATABASE
engine = create_engine(URL_DATABASE_POSTGRESQL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

        
# # cette fonction permet de creer un user a partir de ses identifiants Google
# #------------------------------------------------------
# def create_user(gid: str, email: str, username: str):
#     with psycopg2.connect(**DB_CONFIG) as conn:
#         with conn.cursor() as cur:
#             cur.execute(create_script)
#             insert_user= 'INSERT INTO users (gid, email, username) VALUES (%s, %s, %s)'
#             insert_value= (gid,email,username)
#             cur.execute(insert_user,insert_value)

# cette fonction permet de creer un user a partir de ses identifiants Google
def createUser(google_user : GoogleUser):
    pass        

# #permet de recuperer tout les utilisateurs de la base de données
#     #------------------------------------------------------  
# def get_all_user():
#     with psycopg2.connect(**DB_CONFIG) as conn:
#         with conn.cursor() as cur:
#             cur.execute('SELECT * FROM users')
#             return cur.fetchall()

# #verifie si un utilisateur est deja dans la base de données 
# #------------------------------------------------------
# def existing_user(gid):
#     with psycopg2.connect(**DB_CONFIG) as conn:
#         with conn.cursor() as cur:
#             cur.execute(existing_table,("users",))
#             if cur.fetchone()[0]:
#                 cur.execute('SELECT * FROM users WHERE gid = %s', (gid,))
#             else:
#                 cur.execute(create_script)
#             cur.execute('SELECT * FROM users WHERE gid = %s', (gid,))
#             return cur.fetchone() is not None
