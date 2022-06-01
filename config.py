DATABASE = {
    "DB_DRIVER": "mysql+pymysql",
    "DB_HOST": "localhost",
    "DB_USER": "unittest_root",
    "DB_PASSWORD": "unittest_pwd",
    "DB_NAME": "token_balance_service_unittest_db",
    "DB_PORT": 3306,
    "DB_LOGGING": True,
}

HTTP_PROVIDER = "https://ropsten.infura.io"
BLOCK_THRESHOLD = 5

SLACK_HOOK = {
    "hostname": "https://hooks.slack.com",
    "port": 443,
    "path": "",
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
}

SNAPSHOT_PRUNE_NUMBER = 0

CARDANO_DB_SYNC_SERVICE_API_BASE_PATH = ""
CARDANO_DB_SYNC_SERVICE_API_KEY = ""
