import numpy as np
from models.project import AlgorithmParameters
from models.experiment_data import ExperimentData


def create_dummy_experiment_data():
    frequency = np.array([1, 10, 100])
    log_relaxation_time = np.log10(1 / frequency)
    real_impedance = np.array([20.5, 30.2, 25.1])
    imaginary_impedance = np.array([5.1, -2.3, 3.5])

    return ExperimentData(
        frequency=frequency,
        logarithmic_relaxation_time=log_relaxation_time,
        real_impedance=real_impedance,
        imaginary_impedance=imaginary_impedance
    )

def create_dummy_algorithm_parameters():
    # your dummy AlgorithmParameters instance creation here
    return AlgorithmParameters(
        runs_num=1,
        max_generations=2,
        mutate_probability=0.3,
        add_probability=0.1,
        stop_criteria=15,
        duplication_factor=4,
        expected_peaks_num=2,
        norm_factor=0.1,
        point_diff=2,
        width_factor=5,
        alpha=0.7,
        use_filter=True,
        population_size=20,
        w0=0.002,
        w1=0.0002,
        initial_functions=[0, 1],
        mutation_functions=[0, 1,2],
        upper_bounds={0:1,1:1,2:1},
        lower_bounds={0:0,1:0,2:0},
    )

dummy_experiment_data = create_dummy_experiment_data()
dummy_algorithm_parameters = create_dummy_algorithm_parameters()
test_project_name = 'testing'