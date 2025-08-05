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
            imaginary_impedance FLOAT,
            normalization_factor FLOAT
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
        normalization_factor = arrays['normalization_factor']
        length = len(arrays['frequency'])

        for i in range(length):
            cursor.execute('''
            INSERT INTO ExperimentData(version, frequency, logarithmic_relaxation_time, real_impedance, imaginary_impedance, normalization_factor)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                version,
                arrays['frequency'][i],
                arrays['logarithmic_relaxation_time'][i],
                arrays['real_impedance'][i],
                arrays['imaginary_impedance'][i],
                normalization_factor
            ))
    conn.commit()
    conn.close()


def get_experiment_data_db(version: int) -> ExperimentData:
    db_path = get_db_path()
    query = '''
    SELECT frequency, logarithmic_relaxation_time, real_impedance, imaginary_impedance, normalization_factor
    FROM ExperimentData
    WHERE version = ?
    ORDER BY frequency ASC
    '''

    with sqlite3.connect(db_path, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (version,))
        results = cursor.fetchall()

    if results:
        frequency_list, logarithmic_relaxation_time_list, real_impedance_list, imaginary_impedance_list, normalization_factor_list = zip(*results)

        return ExperimentData(
            frequency=np.array(frequency_list, dtype=float),
            logarithmic_relaxation_time=np.array(logarithmic_relaxation_time_list, dtype=float),
            real_impedance=np.array(real_impedance_list, dtype=float),
            imaginary_impedance=np.array(imaginary_impedance_list, dtype=float),
            normalization_factor=float(normalization_factor_list[0])  # Same for all rows
        )
    else:
        raise ValueError(f"No data found for version {version}")
