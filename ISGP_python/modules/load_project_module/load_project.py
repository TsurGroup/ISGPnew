from data_base.genomes import  get_generation_best_genome, get_generation_num_in_run_db, get_genome_by_id, get_run_num
from mappers.dashboard_mapper import get_dashboard_view




def get_project_runs_num():
    
    run_num = get_run_num()
    return run_num

def get_runs_generation_num(run_num):

    generation_num = get_generation_num_in_run_db(run_num)

    return generation_num

# def get_project_metadata(run_num,generation_num):
    
#     genome = get_generation_best_genome(run_num,generation_num)

#     dashboard_view = get_dashboard_view(run_num, generation_num, genome)
#     return dashboard_view




def get_generation_data(run_num,generation_num):
    
    genome = get_generation_best_genome(run_num,generation_num)
    print(genome)

    dashboard_view = get_dashboard_view(run_num, generation_num, genome)
    return dashboard_view



def get_genome_data(genome_id):
    
    genome,run,generation = get_genome_by_id(genome_id)
    print(genome)
    
    #discrepencies = get_discrepencies(run,generation)


    dashboard_view = get_dashboard_view(run, generation, genome)
    return dashboard_view