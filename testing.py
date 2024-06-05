import mysql.connector

# Establishing a connection to the MySQL database
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="harvest_hub"
    )
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()

        # Creating the 'users' table
        cursor.execute("CREATE TABLE users (userid INT AUTO_INCREMENT PRIMARY KEY, firstname VARCHAR(255), secondname VARCHAR(255), password VARCHAR(255))")
        print("Table 'users' created successfully.")

except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)

finally:
    # Closing database connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


