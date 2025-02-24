import sqlite3
import os
import sys
import threading
from sqlite3 import Error

from file_managment.file_manager import get_db_path

# Global connection variable
#_db_connections = threading.local()
#db_path = ''

# def get_db_path():
#     return db_path

# def get_executable_dir():
#     if getattr(sys, 'frozen', False):
#         return os.path.dirname(sys.executable)
#     else:
#         return os.path.dirname(os.path.abspath(__file__))
    

# def get_base_dir():
#     if getattr(sys, 'frozen', False):
#         # The application is frozen (running as an executable)
#         return os.path.dirname(sys.executable)
#     else:
#         # The application is running in a normal Python environment
#         return os.path.dirname(os.path.abspath(__file__))


# PROJECTS_DIR = os.path.join(get_base_dir(), "projects")


# def get_db_connection():
#     global db_path
#     print('_db_connections is', _db_connections)
#     print('db_path is', db_path)
#     if not hasattr(_db_connections, 'conn'):
#         # Ensure db_path is set
#         if not db_path:
#             raise RuntimeError("Database path has not been set. Call initialize_db_connection first.")
#         _db_connections.conn = sqlite3.connect(db_path, check_same_thread=False)
#     return _db_connections.conn

# def initialize_db_connection(project_name):
#     global db_path
#     executable_dir = get_executable_dir()
#     data_dir = os.path.join(executable_dir, 'data')

#     if not os.path.exists(data_dir):
#         os.makedirs(data_dir)

#     db_name = f"{project_name}.db"
#     db_path = os.path.join(data_dir, db_name)

#     if os.path.exists(db_path):
#         print(f"Database '{db_name}' already exists.")
#         return False

#     # Create and open a new database connection
#     _db_connections.conn = sqlite3.connect(db_path, check_same_thread=False)
#     print(_db_connections.conn)
#     return True



# def close_db_connection():
#     if hasattr(_db_connections, 'conn'):
#         _db_connections.conn.close()
#         del _db_connections.conn

def create_db():
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        conn.close()
        
        return {"message": f"Database for project '{db_path}' created successfully", "db_path": db_path}
    
    except Error as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An error occurred while creating the project or database at'{db_path}'."}
    