psql -v -U postgres -c "CREATE USER $DB_USER PASSWORD '$DB_PASS'"
psql -v -U postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER"
