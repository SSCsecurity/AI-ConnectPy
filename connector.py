import os
import psycopg2

# Direct connection string (gets picked up by ConnectionStringScanner)
conn = psycopg2.connect("postgres://appuser:s3cr3t@prod-db.internal.company.com:5432/customers_prod")

# Env var reference (gets picked up by EnvVarPatternScanner)
db_url = os.getenv("DATABASE_URL")
redis_host = os.environ.get("REDIS_HOST")
