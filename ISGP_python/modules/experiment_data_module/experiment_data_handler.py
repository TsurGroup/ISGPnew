from io import BytesIO
from fastapi import UploadFile
import numpy as np
from data_base.experiment_data import insert_experiment_data
from modules.experiment_data_module.kkt_module import get_kkt_graph
from cache.cache import set_experiment_data, set_project_constants
from models.experiment_data import ExperimentData
from modules.experiment_data_module.constant_data import calculate_constant_data
import pandas as pd


async def new_save_experiment_data(file1: UploadFile, file2: UploadFile):
    file1_data = await file1.read()
    file2_data = await file2.read()

    # Determine the file type and handle each file accordingly
    data_set1 = get_data_from_file(file1, file1_data)
    data_set2 = get_data_from_file(file2, file2_data)
    
    #project_constants = calculate_constant_data(data_set1,data_set2)
    #set_project_constants(project_constants)

    insert_experiment_data(data_set1, 0)
    insert_experiment_data(data_set2, 1)
    
    kkt_graph1 = get_kkt_graph(0)
    kkt_graph2 = get_kkt_graph(1)
    return kkt_graph1, kkt_graph2

def get_data_from_file(file: UploadFile, file_data: bytes):
    
    experiment_data = ExperimentData()
    if file.filename.endswith('.xlsx'):
        experiment_data =  get_data_from_excel(file_data)
    else:
        experiment_data = get_data_from_text(file_data)

    normalize_impedance(experiment_data)
    return experiment_data

def get_data_from_excel(file_data: bytes):
    # Wrap the bytes in a BytesIO object and load the Excel file into a DataFrame
    df = pd.read_excel(BytesIO(file_data))

    # Sort the DataFrame by the "Freq" column in ascending order
    df_sorted = df.sort_values(by="Freq").reset_index(drop=True)

    experiment_data = ExperimentData()
    experiment_data.frequency = df_sorted["Freq"].values
    experiment_data.real_impedance = df_sorted["Z' (a)"].values
    experiment_data.imaginary_impedance = df_sorted["Z'' (b)"].values
    experiment_data.logarithmic_relaxation_time = np.log10(1 / (2 * np.pi * experiment_data.frequency))

    return experiment_data

def get_data_from_text(file_data: bytes):
    data = np.loadtxt(file_data.decode('utf-8').splitlines(), delimiter="\t")

    # Sort the data by the first column (frequency)
    data_sorted = data[data[:, 0].argsort()]

    experiment_data = ExperimentData()
    experiment_data.frequency = data_sorted[:, 0]  # First column
    experiment_data.real_impedance = data_sorted[:, 1]  # Second column
    experiment_data.imaginary_impedance = data_sorted[:, 2]  # Third column
    experiment_data.logarithmic_relaxation_time = np.log10(1 / (2 * np.pi * experiment_data.frequency))

    return experiment_data

def normalize_impedance(experiment_data:ExperimentData):
    kramers_kronig_transform = max(experiment_data.real_impedance)
    experiment_data.real_impedance /= kramers_kronig_transform
    experiment_data.imaginary_impedance /= kramers_kronig_transform

