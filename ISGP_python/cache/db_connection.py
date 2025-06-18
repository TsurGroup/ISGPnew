import sqlite3
import os
import sys
import threading
from sqlite3 import Error

from file_managment.file_manager import get_db_path


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
    