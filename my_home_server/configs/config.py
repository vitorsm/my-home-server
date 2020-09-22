import os

HOST_PORT = 5000

# ======================================================================================================
# Database configurations
# Description:
# ======================================================================================================

DB_URL = os.environ.get("DB_URL", "localhost:3306/myhome")
DB_USERNAME = os.environ.get("DB_USERNAME", "user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

DB_CONNECTION_STR = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}"

# ======================================================================================================
# Security configurations
# Description:
# ======================================================================================================

ENCRYPT_SECRET_KEY = os.environ.get("ENCRYPT_SECRET_KEY", "TMMcUgCsu5qbYmJ2Qbcw")
HOURS_TO_EXPIRATION_TOKEN = int(os.environ.get("HOURS_TO_EXPIRATION_TOKEN", "12"))

# ======================================================================================================
# Repositories configurations
# Description:
# ======================================================================================================

LOG_REPOSITORY = "/var/log/myhome-server"
