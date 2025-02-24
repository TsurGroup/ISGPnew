from models.project import AlgorithmParameters, AlgorithmParametersView


def get_algorithm_parameters_from_view(algorithim_parameters_view: AlgorithmParametersView):

    algorithm_parameters = AlgorithmParameters()
    algorithm_parameters.runs_num = algorithim_parameters_view.runsNum
    algorithm_parameters.max_generations = algorithim_parameters_view.maxGenerations
    algorithm_parameters.mutate_probability = algorithim_parameters_view.mutateProbability
    algorithm_parameters.add_probability = algorithim_parameters_view.addProbability
    algorithm_parameters.norm_factor = algorithim_parameters_view.normFactor
    algorithm_parameters.point_diff = algorithim_parameters_view.pointDiff
    algorithm_parameters.width_factor = algorithim_parameters_view.widthFactor
    algorithm_parameters.alpha = algorithim_parameters_view.alpha

    algorithm_parameters.initial_functions = algorithim_parameters_view.initialFunctions    
    algorithm_parameters.mutation_functions = algorithim_parameters_view.mutationFunctions




    return algorithm_parameters




 