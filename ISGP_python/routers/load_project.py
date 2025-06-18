from fastapi import APIRouter, Depends

from data_base.genomes import get_generation_genomes_id, get_genome_by_id
from modules.load_project_module.load_project import get_generation_data, get_genome_data, get_project_runs_num,get_runs_generation_num
from project_context import get_current_project_name

router = APIRouter()

@router.get("/getRunNum")
async def get_run_num(project_name: str = Depends(get_current_project_name)):
    runs_num =  get_project_runs_num()
    return runs_num

@router.get("/getRunsGenerationNum/{run_num}")
async def get_runs_generation_num_endpoint(run_num:int,project_name: str = Depends(get_current_project_name)):
    generation_num =  get_runs_generation_num(run_num)
    return generation_num

@router.get("/getGenerationModels/{run_num}/{generation_num}")
async def get_generation_models(run_num:int,generation_num:int,project_name: str = Depends(get_current_project_name)):
    genomes = get_generation_genomes_id(run_num,generation_num)

    return genomes

# @router.get("/getGenerationModel/{run_num}/{generation_num}")
# async def get_generation_model(run_num:int,generation_num:int,project_name: str = Depends(get_current_project_name)):
#     dashboard_view = get_generation_data(run_num,generation_num)

#     return dashboard_view


@router.get("/getModel/{genome_id}")
async def get_genome_model(genome_id:int,project_name: str = Depends(get_current_project_name)):
    genome = get_genome_data(genome_id)

    return genome
