import sqlite3

import numpy as np
from models.experiment_data import ExperimentData
from file_managment.file_manager import get_db_path


def create_experiment_table():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    with conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ExperimentData(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version INTEGER,
            frequency FLOAT,
            logarithmic_relaxation_time FLOAT,
            real_impedance FLOAT,
            imaginary_impedance FLOAT
        )
        ''')
    conn.commit()
    conn.close()


def insert_experiment_data(experiment_data, version):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    with conn:
        cursor = conn.cursor()
        arrays = experiment_data.to_dict()
        length = len(arrays['frequency'])

        for i in range(length):
            cursor.execute('''
            INSERT INTO ExperimentData(version, frequency, logarithmic_relaxation_time, real_impedance, imaginary_impedance)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                version,
                arrays['frequency'][i],
                arrays['logarithmic_relaxation_time'][i],
                arrays['real_impedance'][i],
                arrays['imaginary_impedance'][i]
            ))
    conn.commit()
    conn.close()


def get_experiment_data_db(version: int) -> ExperimentData:
    db_path = get_db_path()  # Ensure this function returns the path to your SQLite database
    query = '''
    SELECT frequency, logarithmic_relaxation_time, real_impedance, imaginary_impedance
    FROM ExperimentData
    WHERE version = ?
    ORDER BY frequency ASC
    '''
    
    with sqlite3.connect(db_path, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (version,))
        results = cursor.fetchall()
    
    if results:
        # Assuming each column contains lists of values
        frequency_list, logarithmic_relaxation_time_list, real_impedance_list, imaginary_impedance_list = zip(*results)
        
        # Convert lists to numpy arrays
        frequency_array = np.array(frequency_list, dtype=float)
        logarithmic_relaxation_time_array = np.array(logarithmic_relaxation_time_list, dtype=float)
        real_impedance_array = np.array(real_impedance_list, dtype=float)
        imaginary_impedance_array = np.array(imaginary_impedance_list, dtype=float)
        
        return ExperimentData(
            frequency=frequency_array,
            logarithmic_relaxation_time=logarithmic_relaxation_time_array,
            real_impedance=real_impedance_array,
            imaginary_impedance=imaginary_impedance_array
        )
    else:
        raise ValueError(f"No data found for version {version}")