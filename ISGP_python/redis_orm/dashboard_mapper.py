# import numpy as np

# from models.experiment_data import ExperimentData
# from view_models.graph_view import PointData
# from view_models.dashboard_view import DashboardView, DiscrepancyGraph,ImpadanceGraphView, ModelGraphView,ResidualGraphView

# from modules.genetic_algorithm.genome_parameters import Genome, simpson_matrix

# from redis_orm.redis_client import get_best_models, get_data_set, get_discrepancies

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
#     modelGraph = ModelGraphView()
    

#     for index, t in enumerate(time_samples):
#        point = PointData()
#        point.x = t
#        point.y = solution_sampels[index]
#        modelGraph.model.append(point)
    
#     return modelGraph


# def get_discrepancy_graph(user_id,genome:Genome):
#     discrepancy_graph = DiscrepancyGraph()
#     discrepancies = get_discrepancies(user_id)
#    # print(discrepancies)
#     for discrepancy in discrepancies:
#        #print(discrepancy)
#        point = PointData()
#        point.x = discrepancy['parameters_num']
#        point.y = discrepancy['discrepancy']
#        discrepancy_graph.allDiscrepancies.append(point)
    

#     point = PointData()
#     point.x = genome.get_parameters_num()
#     point.y = genome.discrepancy
#     discrepancy_graph.currentModel.append(point)
    
#     best_models = get_best_models(user_id)
#     for model in best_models:
#        #print(discrepancy)
#        point = PointData()
#        point.x = model.get_parameters_num()
#        point.y = model.discrepancy
#        discrepancy_graph.bestModels.append(point)

#     return discrepancy_graph



# def get_dashboard_view(user_id,generation,genome:Genome):

#     dashboard_view = DashboardView()

#     dashboard_view.generation = generation + 1
#     dashboard_view.fitness = round(genome.new_fitness, 5)
#     dashboard_view.modelString = genome.get_latex_string()

#     experiment_data = get_data_set(user_id,0)
#     project_constants = get_project_constants()
    
  

#     point = -(experiment_data.logarithmic_relaxation_time[0]-experiment_data.logarithmic_relaxation_time[1])/3

#     #point = project_constants.time_samples[1]-project_constants.time_samples[0]
#     area = genome.get_area(project_constants.time_samples,point)
#     dashboard_view.area = round(area, 5)

#     solution_sampels = genome.get_genome_value(project_constants.time_samples)
    
#     dashboard_view.modelGraph = get_solution_graph(project_constants.time_samples,solution_sampels)
    
#     imag , real = simpson_matrix(solution_sampels,project_constants)

#     dashboard_view.impadanceGraphView = get_impadence_graph(experiment_data,experiment_data,real,imag)
    
#     dashboard_view.residualGraph = get_residual_graph_new(real,imag,experiment_data)
#     dashboard_view.discrepancyGraph = get_discrepancy_graph(user_id,genome)   
#     return dashboard_view
