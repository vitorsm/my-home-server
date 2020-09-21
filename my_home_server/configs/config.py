import os

HOST_PORT = 5000

# ======================================================================================================
# Database configurations
# Description:
# ======================================================================================================

DB_URL = os.environ.get("DB_URL", "localhost:3306/rz_panel")
DB_USERNAME = os.environ.get("DB_USERNAME", "user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

DB_CONNECTION_STR = f"mysql+pymysql://{DB_URL}:{DB_USERNAME}@{DB_PASSWORD}"
