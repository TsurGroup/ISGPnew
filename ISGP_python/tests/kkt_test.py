import sys
import os

# Add root to sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.experiment_data_module.kkt_module import kkt
from tests.test_data import dummy_experiment_data


def debug_kkt():
    # Get test data from helper function
    

    # Show what's going in
    print("Frequency:\n", dummy_experiment_data.frequency)
    print("\nReal Impedance:\n", dummy_experiment_data.real_impedance)
    print("\nImaginary Impedance:\n", dummy_experiment_data.imaginary_impedance)

    # Run KKT
    Real_KK, Real_KK1 = kkt(dummy_experiment_data)

    # Show results
    print("\nReal_KK:\n", Real_KK)
    print("\nReal_KK1:\n", Real_KK1)


if __name__ == "__main__":
    debug_kkt()
