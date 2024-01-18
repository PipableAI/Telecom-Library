from telecom_library.database import (
    DatabaseConnector,
    get_database_credentials_from_url,
)

remote_db_url = "postgresql://avi:oXMRAx4bEHS1@ep-hidden-thunder-88154842.us-east-2.aws.neon.tech/monitoringDB?sslmode=require"

remote_db_credentials = get_database_credentials_from_url(remote_db_url)

remote_db_connector = DatabaseConnector(
    host=remote_db_credentials["db_host"],
    port=remote_db_credentials["db_port"],
    database=remote_db_credentials["db_name"],
    user=remote_db_credentials["db_user"],
    password=remote_db_credentials["db_password"],
)

#  Create Tables
# sql_file_path = "./database_files/create_tables.sql"
# with open(sql_file_path, 'r') as file:
#     sql_commands = file.read()
#     remote_db_connector.execute_sql_file(sql_commands)

# # Insert Data In Each Table
# sql_file_path = "./database_files/insert_data.sql"
# with open(sql_file_path, 'r') as file:
#     sql_commands = file.read()
#     remote_db_connector.execute_sql_file(sql_commands)