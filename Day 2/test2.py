from dotenv import load_dotenv
import os

# Load variabel lingkungan dari file .env
load_dotenv()

# Contoh penggunaan variabel lingkungan
print("Database host:", os.environ["DB_HOST"])
print("Database port:", os.environ["DB_PORT"])
print("Secret key:", os.environ["SECRET_KEY"])