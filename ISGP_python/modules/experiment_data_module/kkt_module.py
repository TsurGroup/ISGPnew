import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.interpolate import CubicSpline
from scipy.integrate import quad
from cache.cache import get_experiment_data
from view_models.graph_view import PointData
from view_models.kkt_view import KKTGraph




def get_kkt_graph(data_set_id):
   
 kkt_graph = KKTGraph()
 experiment_data = get_experiment_data(data_set_id)



 #real_kkt,real_kkt1 = kkt_transform(experiment_data.frequency,experiment_data.imaginary_impedance)
 real_kkt,real_kkt1 = kkt(data_set_id)
 imaginary_kkt,imaginary_kkt1 = kkt_transform(experiment_data.frequency,experiment_data.real_impedance)

 #print(real_kkt1)

 for i in range(len(experiment_data.frequency)):
            
            point1 = PointData()
            point1.x = experiment_data.frequency[i]
            point1.y = real_kkt1[i]
            kkt_graph.realToImaginaryGraph.kkTransform.append(point1)

            point2 = PointData()
            point2.x = experiment_data.frequency[i]
            point2.y = experiment_data.real_impedance[i]
            kkt_graph.realToImaginaryGraph.realImpedance.append(point2)


            point3 = PointData()
            point3.x = experiment_data.frequency[i]
            point3.y = -imaginary_kkt1[i]
            kkt_graph.imaginaryToRealGraph.kkTransform.append(point3)

            point4 = PointData()
            point4.x = experiment_data.frequency[i]
            point4.y = -experiment_data.imaginary_impedance[i]
            kkt_graph.imaginaryToRealGraph.imaginaryImpedance.append(point4)


            point5 = PointData()
            point5.x = real_kkt[i]
            point5.y = -imaginary_kkt1[i]
            kkt_graph.coleColeGraph.kkTransform.append(point5)

            point6 = PointData()
            point6.x = experiment_data.real_impedance[i]
            point6.y = -experiment_data.imaginary_impedance[i]
            kkt_graph.coleColeGraph.coleCole.append(point6)

 return kkt_graph



def kkt(data_set_id):

    experiment_data = get_experiment_data(data_set_id)
    angular_frequency = 2 * np.pi * experiment_data.frequency
    imaginary_impedance = -experiment_data.imaginary_impedance

    index = len(angular_frequency)
    rkk = np.zeros(index)
    Real_KK = np.zeros(index)
    Real_KK1 = np.zeros(index)

    for m in range(index):
        for k in range(index):
            # Condition for k != m
            if k != m:
                rkk[k] = (angular_frequency[k] * imaginary_impedance[k] - angular_frequency[m] * imaginary_impedance[m]) / (angular_frequency[k]**2 - angular_frequency[m]**2)
            # Condition for diagonal elements in the middle
            elif k == m and k != 0 and k != index - 1:
                rkk[k] = 0.5 * (imaginary_impedance[k] / angular_frequency[k] + (imaginary_impedance[k + 1] - imaginary_impedance[k - 1]) / (angular_frequency[k + 1] - angular_frequency[k - 1]))
            # Condition for the first diagonal element
            elif k == m and k == 0:
                rkk[k] = 0.5 * (imaginary_impedance[k] / angular_frequency[k] + (imaginary_impedance[k + 1] - imaginary_impedance[k]) / (angular_frequency[k + 1] - angular_frequency[k]))
            # Condition for the last diagonal element
            elif k == m and k == index - 1:
                rkk[k] = 0.5 * (imaginary_impedance[k] / angular_frequency[k] + (imaginary_impedance[k] - imaginary_impedance[k - 1]) / (angular_frequency[k] - angular_frequency[k - 1]))

        # Spline approximation and integration
        cs = CubicSpline(angular_frequency, rkk)
        Re_KK1 = cs.integrate(angular_frequency[0], angular_frequency[-1])

        # Numerical integration (Trapezoidal)
        ReKK = 0
        for mm in range(index - 1):
            trap = (rkk[mm + 1] + rkk[mm]) / 2
            dw = angular_frequency[mm + 1] -angular_frequency[mm]
            ReKK += trap * dw
        
        Real_KK[m] = (2 / np.pi) * ReKK + experiment_data.real_impedance[-1]
        Real_KK1[m] = (2 / np.pi) * Re_KK1 + experiment_data.real_impedance[-1]


    return Real_KK,Real_KK1








def kkt_transform(frequency, impedance):
    angular_frequency = 2 * np.pi * frequency
    index = len(angular_frequency)
    KK = np.zeros(index)
    KK1 = np.zeros(index)
    KK_result = np.zeros(index)
    KK1_result= np.zeros(index)
    
    for m in range(index):
        for k in range(index):
            if k != m:
                KK[k] = (impedance[k] - impedance[m]) / (angular_frequency[k]**2 - angular_frequency[m]**2)
            elif k == m:
                if k == 0:
                    KK[k] = (impedance[k+1] - impedance[k]) / (angular_frequency[k+1] - angular_frequency[k]) / (2 * angular_frequency[k])
                elif k == index - 1:
                    KK[k] = (impedance[k] - impedance[k-1]) / (angular_frequency[k] - angular_frequency[k-1]) / (2 * angular_frequency[k])
                else:
                    KK[k] = (impedance[k+1] - impedance[k-1]) / (angular_frequency[k+1] - angular_frequency[k-1]) / (2 * angular_frequency[k])

        # Spline interpolation using UnivariateSpline with no smoothing
        cs = UnivariateSpline(angular_frequency, KK, s=0)

        # Numerical integration of the spline
        integral_value = cs.integral(angular_frequency[0], angular_frequency[-1])

        # Trapezoidal rule integration
        KK_sum = 0
        for mm in range(index - 1):
            trap = (KK[mm + 1] + KK[mm]) / 2
            dw = angular_frequency[mm + 1] - angular_frequency[mm]
            KK_sum += trap * dw

        KK_result[m] = (2 * angular_frequency[m] / np.pi) * KK_sum  #isnt used
        KK1_result[m] = (2 * angular_frequency[m] / np.pi) * integral_value

    return KK_result, KK1_result





