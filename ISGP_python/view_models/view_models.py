# import bisect
# import numpy as np
# from typing import List
# from pydantic import BaseModel, ImportString
# from typing import Optional

# from models.experiment_data import ExperimentData
# from modules.DataHandler.constant_data import get_project_constants
# from modules.GeneticAlgorithim.genome_parameters import Genome, simpson_matrix
# from redis_orm.redis_client import get_data_set, get_discrepancies

# class PointData(BaseModel):
#     x: float = 0
#     y: float = 0

# # class ThreePointData(BaseModel):
# #     xValue: float = 0
# #     y1Value: Optional[float] = None
# #     y2Value: Optional[float] = None
# #     y3Value: Optional[float] = None

# class ImpadanceGraphView(BaseModel):
#     dataset1: list[PointData] = []
#     dataset2: list[PointData] = []
#     model: list[PointData] = []

# class ResidualGraphView(BaseModel):
#     dataset1: list[PointData] = []
#     dataset2: list[PointData] = []

# class DiscrepancyGraph(BaseModel):
#     allSolutions: list[PointData] = []
#     bestSolutions: list[PointData] = []
#     bestSolution: list[PointData] = []
   

# class DashboardView(BaseModel):
#     generation: int = 0
#     fitness: float = 0
#     area: float = 0
#     solutionString:ImportString = ''
#     solutionGraph:  list[PointData] = []
#     #impedanceGraph: list[ThreePointData] = []
#      #residualGraph: list[ThreePointData] = []
#     impadanceGraphView:ImpadanceGraphView = ImpadanceGraphView()
#     residualGraph: ResidualGraphView = ResidualGraphView()
#     discrepancyGraph:DiscrepancyGraph = DiscrepancyGraph()

# def indices_of_values(list1, list2, list3):
#     combined_dict = {}
    
#     # Preprocess indices for list1
#     indices1 = {value: index for index, value in enumerate(list1)}
#     # Preprocess indices for list2
#     indices2 = {value: index for index, value in enumerate(list2)}
#     # Preprocess indices for list3
#     indices3 = {value: index for index, value in enumerate(list3)}
    
#     # Get the maximum length among the three lists
#     max_length = max(len(list1), len(list2), len(list3))
    
#     for index in range(max_length):
#         value1 = list1[index] if index < len(list1) else None
#         value2 = list2[index] if index < len(list2) else None
#         value3 = list3[index] if index < len(list3) else None
        
#         combined_dict[value1] = [indices1.get(value1), indices2.get(value1), indices3.get(value1)]
#         combined_dict[value2] = [indices1.get(value2), indices2.get(value2), indices3.get(value2)]
#         combined_dict[value3] = [indices1.get(value3), indices2.get(value3), indices3.get(value3)]
    
#     return combined_dict

# def indices_of_values_test(list1, list2):
#     combined_dict = {}
    
#     # Preprocess indices for list1
#     indices1 = {value: index for index, value in enumerate(list1)}
#     # Preprocess indices for list2
#     indices2 = {value: index for index, value in enumerate(list2)}
#     # Preprocess indices for list3
    
#     # Get the maximum length among the three lists
#     max_length = max(len(list1), len(list2))
    
#     for index in range(max_length):
#         value1 = list1[index] if index < len(list1) else None
#         value2 = list2[index] if index < len(list2) else None
       
        
#         combined_dict[value1] = [indices1.get(value1), indices2.get(value1)]
#         combined_dict[value2] = [indices1.get(value2), indices2.get(value2)]
       
    
#     return dict(sorted(combined_dict.items()))


# # def get_impadence_graph_data(real_impadance1, imaginary_impadence1, real_impadance2, imaginary_impadence2, solutin_x, solution_y):
# #     data = []
# #     sorted_x_values = indices_of_values(real_impadance1, real_impadance2, solutin_x)

# #     for x_value, indices in sorted_x_values.items():
# #         point = ThreePointData()
# #         point.xValue = x_value
# #         if indices[0] is not None:
# #             point.y1Value = -imaginary_impadence1[indices[0]]
# #         if indices[1] is not None:
# #             point.y2Value = -imaginary_impadence2[indices[1]]
# #         if indices[2] is not None:
# #             point.y3Value = -solution_y[indices[2]]
# #         data.append(point)
    
# #     data.sort(key=lambda x: x.xValue, reverse=False)
# #     return data

# def get_impadence_graph(experiment_data1:ExperimentData,experiment_data2:ExperimentData, solutin_x, solution_y):
     
#     data = ImpadanceGraphView()

#     for i in range(len(experiment_data1.real_impedance)):
            
#             dataset1_point = PointData()
#             dataset1_point.x = round(experiment_data1.real_impedance[i],4)
#             dataset1_point.y = round(-experiment_data1.imaginary_impedance[i],4)
#             data.dataset1.append(dataset1_point)

#             dataset2_point = PointData()
#             dataset2_point.x = round(experiment_data2.real_impedance[i],4)
#             dataset2_point.y = round(-experiment_data1.imaginary_impedance[i],4)
#             data.dataset2.append(dataset2_point)
     

#     for i in range(len(experiment_data1.real_impedance)):
            
#             model_point = PointData()
#             model_point.x = round(solutin_x[i],4)
#             model_point.y = round(-solution_y[i],4)
#             data.model.append(model_point)

            

#     return data

    

# # def get_impadence_graph_const_data(real_impadance1, imaginary_impadence1, real_impadance2, imaginary_impadence2):
# #      data = []
# #      sorted_x_values = indices_of_values_test(real_impadance1, real_impadance2)

# #      for x_value, indices in sorted_x_values.items():
# #          point = ThreePointData()
# #          point.xValue = round(x_value, 4)
# #          if indices[0] is not None:
# #             point.y1Value = round(-imaginary_impadence1[indices[0]], 4)
# #          if indices[1] is not None:
# #              point.y2Value = round(-imaginary_impadence2[indices[1]], 4)
        
# #          data.append(point)
    
# #      data.sort(key=lambda x: x.xValue, reverse=False)
# #      return data

# # def get_residual_graph(solution_real,solution_img,experiment_data:ExperimentData):
# #     residualGraph = []
# #     radius = np.sqrt(experiment_data.imaginary_impedance**2+experiment_data.real_impedance**2)
    
# #     residual_re = (solution_real-experiment_data.real_impedance)/radius
# #     residual_im = (solution_img-experiment_data.imaginary_impedance)/radius
    

# #     for index, t in enumerate(experiment_data.logarithmic_relaxation_time):
# #        point = ThreePointData()
# #        point.xValue = t
# #        point.y1Value = residual_im[index]
# #        point.y2Value = residual_re[index]
# #        residualGraph.append(point)

# #     return residualGraph

# def get_residual_graph_new(solution_real,solution_img,experiment_data:ExperimentData):
   
#     residualGraph = ResidualGraphView()
#     radius = np.sqrt(experiment_data.imaginary_impedance**2+experiment_data.real_impedance**2)
    
#     residual_re = (solution_real-experiment_data.real_impedance)/radius
#     residual_im = (solution_img-experiment_data.imaginary_impedance)/radius
    

#     for index, t in enumerate(experiment_data.logarithmic_relaxation_time):
       
#         dataset1_point = PointData()
#         dataset1_point.x = round(-t,4)
#         dataset1_point.y = round(residual_im[index],4)
#         residualGraph.dataset1.append(dataset1_point)

#         dataset2_point = PointData()
#         dataset2_point.x = round(-t,4)
#         dataset2_point.y = round(residual_re[index],4)
#         residualGraph.dataset2.append(dataset2_point)

#     return residualGraph

# def get_solution_graph(time_samples,solution_sampels):
#     solutionGraph = []

#     for index, t in enumerate(time_samples):
#        point = PointData()
#        point.x = t
#        point.y = solution_sampels[index]
#        solutionGraph.append(point)

#     return solutionGraph


# def get_discrepancy_graph(user_id):
#     discrepancy_graph = DiscrepancyGraph()
#     discrepancies = get_discrepancies(user_id)
#    # print(discrepancies)
#     for discrepancy in discrepancies:
#        #print(discrepancy)
#        point = PointData()
#        point.x = discrepancy['parameters_num']
#        point.y = discrepancy['discrepancy']
#        discrepancy_graph.allSolutions.append(point)

#     return discrepancy_graph



# def get_dashboard_view(user_id,generation,genome:Genome):

#     dashboard_view = DashboardView()

#     dashboard_view.generation = generation + 1
#     dashboard_view.fitness = round(genome.new_fitness, 5)
#     dashboard_view.solutionString = genome.get_latex_string()

#     experiment_data = get_data_set(user_id,0)
#     project_constants = get_project_constants()
    
#     point = project_constants.time_samples[1]-project_constants.time_samples[0]
#     area = genome.get_area(project_constants.time_samples,point)
#     dashboard_view.area = round(area, 5)

#     solution_sampels = genome.get_genome_value(project_constants.time_samples)
    
#     dashboard_view.solutionGraph = get_solution_graph(project_constants.time_samples,solution_sampels)
    
#     imag , real = simpson_matrix(solution_sampels,project_constants)

#     dashboard_view.impadanceGraphView = get_impadence_graph(experiment_data,experiment_data,real,imag)
    
#     dashboard_view.residualGraph = get_residual_graph_new(real,imag,experiment_data)
#     dashboard_view.discrepancyGraph = get_discrepancy_graph(user_id)   
#     return dashboard_view
    
    


    
#     #dashboard_view.impedanceGraph = get_impadence_graph_data(experiment_data.real_impedance,experiment_data.imaginary_impedance,
#                               #       experiment_data.real_impedance,experiment_data.imaginary_impedance,
#                                #      real,imag)