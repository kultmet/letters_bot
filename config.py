import os
from dotenv import load_dotenv

load_dotenv()


db_name = os.getenv('DB_NAME', default='postgres')
db_user = os.getenv('DB_USERNAME', default='postgres')
db_pass = os.getenv('DB_PASSWORD', default='postgres')
db_host = os.getenv('DB_HOST', default='localhost')
db_port = os.getenv('DB_PORT', default='5432')