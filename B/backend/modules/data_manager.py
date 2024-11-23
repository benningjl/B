import psycopg2
from psycopg2 import sql
from datetime import datetime

class DataManager:
    def __init__(self, db_config):
        self.db_config = db_config

    def _get_connection(self):
        """Establish a connection to the database."""
        connection = psycopg2.connect(**self.db_config)
        return connection

    def insert_data(self, table, data):
        """Insert data into the specified table."""
        try:
            # Debugging: print the data to check if it's a dictionary
            print("Data passed to insert_data:", data)
            
            # Check if 'data' is a dictionary
            if not isinstance(data, dict):
                raise ValueError("Data must be a dictionary of column-value pairs")

            columns = data.keys()
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(map(sql.Placeholder, columns))
            )

            # Debugging: Print the final SQL query
            print("SQL Query:", query.as_string(self._get_connection()))
            
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    # Pass the data dictionary directly, not as a list
                    cursor.execute(query, data)
                    conn.commit()
                    print("Data inserted successfully.")
        except Exception as e:
            print(f"An error occurred while inserting data: {e}")

    def select_data(self, table):
        """Select all data from the specified table."""
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table))
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    data = cursor.fetchall()
                    print(data)
        except Exception as e:
            print(f"An error occurred while selecting data: {e}")

    def update_data(self, table, data, condition):
        """Update data in the specified table based on a condition."""
        try:
            set_columns = data.keys()
            set_values = [data[column] for column in set_columns]
            condition_column = list(condition.keys())[0]
            condition_value = list(condition.values())[0]
            
            query = sql.SQL("UPDATE {} SET {} WHERE {} = %s").format(
                sql.Identifier(table),
                sql.SQL(', ').join(
                    [sql.Identifier(col) + sql.SQL(" = %s") for col in set_columns]
                ),
                sql.Identifier(condition_column)
            )

            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, set_values + [condition_value])
                    conn.commit()
                    print("Data updated successfully.")
        except Exception as e:
            print(f"An error occurred while updating data: {e}")

    def delete_data(self, table, condition):
        """Delete data from the specified table based on a condition."""
        try:
            condition_column = list(condition.keys())[0]
            condition_value = list(condition.values())[0]
            query = sql.SQL("DELETE FROM {} WHERE {} = %s").format(
                sql.Identifier(table),
                sql.Identifier(condition_column)
            )

            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, [condition_value])
                    conn.commit()
                    print("Data deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting data: {e}")

# Example usage
if __name__ == "__main__":
    db_config = {
        'dbname': 'app_database',
        'user': 'postgres',
        'password': '123456',
        'host': 'localhost',
        'port': '5432'
    }
    
    data_manager = DataManager(db_config)
    
    # Example: Insert data (make sure to pass a dictionary with column names and values)
    data = {"username": "johndoe", "email": "johndoe@example.com"}
    data_manager.insert_data("users", data)
    
    # Select data example
    data_manager.select_data("users")
    
    # Update data example
    update_data = {"email": "john.newemail@example.com"}
    condition = {"username": "johndoe"}
    data_manager.update_data("users", update_data, condition)
    
    # Delete data example
    delete_condition = {"username": "johndoe"}
    data_manager.delete_data("users", delete_condition)
