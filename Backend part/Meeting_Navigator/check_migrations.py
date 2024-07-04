import sqlite3

# Path to your SQLite database file
db_path = 'db.sqlite3'


def check_migrations(app_name):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute the query to check migrations for the specified app
        cursor.execute(f"SELECT * FROM django_migrations WHERE app='{app_name}'")
        rows = cursor.fetchall()

        # Print the results
        for row in rows:
            print(row)

        # Close the connection
        conn.close()
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")


if __name__ == "__main__":
    app_name = 'base'  # Replace 'base' with your Django app name
    check_migrations(app_name)
