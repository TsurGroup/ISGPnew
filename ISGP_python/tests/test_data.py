import math
import numpy as np
import pandas as pd
from models.functions.function import FunctionType
from models.project import AlgorithmParameters
from models.experiment_data import ExperimentData

def get_data_from_excel_path(file_path: str):
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read Excel file from path: {e}")

    required_columns = {"Freq", "Z' (a)", "Z'' (b)"}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    df_sorted = df.sort_values(by="Freq").reset_index(drop=True)

    experiment_data = ExperimentData()
    experiment_data.frequency = df_sorted["Freq"].values
    experiment_data.real_impedance = df_sorted["Z' (a)"].values
    experiment_data.imaginary_impedance = df_sorted["Z'' (b)"].values
    experiment_data.logarithmic_relaxation_time = np.log10(1 / (2 * np.pi * experiment_data.frequency))

    return experiment_data


def create_dummy_experiment_data():
   #file_path = r"C:\Users\shema\OneDrive\Desktop\ISGP Data\Aala_data1.xlsx"
   file_path = r"C:\Users\shema\OneDrive\Desktop\ISGP Data\DataExcel.xlsx"
   experiment_data = get_data_from_excel_path(file_path)
   experiment_data.normalization_factor = max(experiment_data.real_impedance)
   experiment_data.real_impedance /= experiment_data.normalization_factor
   experiment_data.imaginary_impedance /= experiment_data.normalization_factor
   return experiment_data

    # frequency = np.array([1, 10, 100])
    # log_relaxation_time = np.log10(1 / frequency)
    # real_impedance = np.array([20.5, 30.2, 25.1])
    # imaginary_impedance = np.array([5.1, -2.3, 3.5])

    # return ExperimentData(
    #     frequency=frequency,
    #     logarithmic_relaxation_time=log_relaxation_time,
    #     real_impedance=real_impedance,
    #     imaginary_impedance=imaginary_impedance
    # )

def create_dummy_algorithm_parameters():
    # your dummy AlgorithmParameters instance creation here
    algorithm_parameters =  AlgorithmParameters(
        runs_num=1,
        max_generations=7,
        mutate_probability=0.3,
        add_probability=0.1,
        stop_criteria=15,
        duplication_factor=4,
        expected_peaks_num=2,
        norm_factor=0.1,
        point_diff=3,
        width_factor=5,
        alpha=0.7,
        use_filter=False,
        population_size=20,
        w0=0.002,
        w1=0.0002,
        initial_functions=[0, 1],
        mutation_functions=[0, 1,2],
        upper_bounds={0:1,1:1,2:1},
        lower_bounds={0:0,1:0,2:0},
    )
    tau_max = np.ceil(dummy_experiment_data.logarithmic_relaxation_time[0])
    tau_min = -math.ceil(-dummy_experiment_data.logarithmic_relaxation_time[-1]) 
    pos_tau = 0.8*dummy_experiment_data.logarithmic_relaxation_time[0]+0.2*dummy_experiment_data.logarithmic_relaxation_time[0]##not sure y is called this. u should change and call it something else

    upper_bounds = {func.value: pos_tau for func in FunctionType}## this should be the normalization factor which is the max of real impadance(kk kroning)
    lower_bounds = {func.value: tau_min for func in FunctionType}


    upper_bounds[FunctionType.NegativePseudoDelta.value] = tau_max
    upper_bounds[FunctionType.NegativeGaussian.value] = tau_max
    upper_bounds[FunctionType.NegativeLorentzian.value] = tau_max
    upper_bounds[FunctionType.NegativeHyperbolicSecant.value] = tau_max

    lower_bounds[FunctionType.NegativePseudoDelta.value] = pos_tau
    lower_bounds[FunctionType.NegativeGaussian.value] = pos_tau
    lower_bounds[FunctionType.NegativeLorentzian.value] = pos_tau
    lower_bounds[FunctionType.NegativeHyperbolicSecant.value] = pos_tau

    upper_bounds[FunctionType.LeftPseudoDelta.value] = tau_max+3
    upper_bounds[FunctionType.RightPseudoDelta.value] = tau_min-3

    lower_bounds[FunctionType.LeftPseudoDelta.value] = tau_max+1.5
    lower_bounds[FunctionType.RightPseudoDelta.value] = tau_min-4

    algorithm_parameters = AlgorithmParameters(upper_bounds=upper_bounds,lower_bounds=lower_bounds)

    algorithm_parameters.width_factor  = -(dummy_experiment_data.logarithmic_relaxation_time[-1] - dummy_experiment_data.logarithmic_relaxation_time[0])

    algorithm_parameters.initial_functions = [0]
    #algorithm_parameters.mutation_functions= [0,1,2,3]
    algorithm_parameters.mutation_functions= [0,1]
    return algorithm_parameters

dummy_experiment_data = create_dummy_experiment_data()
dummy_algorithm_parameters = create_dummy_algorithm_parameters()
test_project_name = 'RCdataTest'