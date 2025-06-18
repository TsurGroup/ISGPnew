import json
import sqlite3

from file_managment.file_manager import get_db_path

from models.functions.asymmetric_gaussian import AsymmetricGaussian
from models.functions.asymmetric_hyperbolic_secant import AsymmetricHyperbolicSecant
from models.functions.asymmetric_lorentzian import AsymmetricLorentzian
from models.functions.cole_cole import ColeCole
from models.functions.gaussian import Gaussian
from models.functions.havriliak_negami import HavriliakNegami
from models.functions.hyperbolic_secant import HyperbolicSecant
from models.functions.kirkwood_fuoss import KirkwoodFuoss
from models.functions.lorentzian import Lorentzian
from models.functions.losev import Losev
from models.functions.pearson_vii import PearsonVII
from models.functions.pseudo_delta import PseudoDelta
from models.functions.pseudo_voigt import PseudoVoigt

from models.experiment_data import ExperimentData
from models.functions.function import Function, FunctionParameters, FunctionType
from models.genome import Genome

def create_genomes_table():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    with conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Genome (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run INTEGER,
            generation INTEGER,
            fitness FLOAT,
            discrepancy FLOAT,
            parameters_num INTEGER,
            area_penalty FLOAT,
            peakes_width_penalty FLOAT,
            peakes_num_penalty FLOAT,
            free_parameters_penalty FLOAT,
            compatibility_penalty FLOAT,
            best_model BOOLEAN,            
            functions TEXT
        )
        ''')
    conn.commit()
    conn.close()

        
def save_genomes(run:int,generation: int,genomes: list[Genome]):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    with conn:
        cursor = conn.cursor()
        for i, genome in enumerate(genomes):
            best_model = 1 if i == 0 else 0  # 1 for True, 0 for False
            cursor.execute('''
              INSERT INTO Genome (
               run,
              generation, 
              fitness, 
              discrepancy, 
              parameters_num,
              area_penalty, 
              peakes_width_penalty, 
              peakes_num_penalty, 
              free_parameters_penalty, 
              compatibility_penalty,  
              best_model, 
              functions
              ) VALUES (?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?)
              ''', (
             run,
             generation,
             genome.fitness,
             genome.discrepancy,
             genome.get_parameters_num(),
             genome.area_penalty,
             genome.peakes_width_penalty,
             genome.peakes_num_penalty,
             genome.free_parameters_penalty,
             genome.compatibility_penalty,
             best_model,
    json.dumps([func.to_dict() for func in genome.functions])  # Serialize functions
))
    conn.commit()
    conn.close()

def get_run_num():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    with conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT run FROM Genome
        ORDER BY id DESC
        LIMIT 1
        ''')
        result = cursor.fetchone()
    return result[0] if result else None

def get_generation_num_in_run_db(run_number):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    with conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT generation FROM Genome
        WHERE run = ?
        ORDER BY generation DESC
        LIMIT 1
        ''', (run_number,))
        result = cursor.fetchone()
    return result[0] if result else None

    
def get_generation_genomes_id(run: int, generation: int):
    db_path = get_db_path()  # Ensure this function returns the correct database path
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, compatibility_penalty, best_model 
            FROM Genome 
            WHERE run = ? AND generation = ?
            ORDER BY best_model DESC, id ASC  -- Ensure best_model=True comes first
        ''', (run, generation))
        genome_data = cursor.fetchall()
        
        # Returning a dictionary with id as the key and fitness as the value
        return {genome[0]: genome[1] for genome in genome_data} if genome_data else {}
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {}  # Return an empty dictionary in case of an error
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}  # Ensure empty dictionary is returned for any unexpected errors
    
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

def get_discrepencies_from_db(run: int, max_generation: int):
    db_path = get_db_path()  # Assuming this function gives the correct path to the database
    #print(run)
    #print(max_generation)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # This ensures rows are returned as dictionaries

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT discrepancy, parameters_num, best_model
                FROM Genome
                WHERE run = ? AND generation < ?
            ''', (run, max_generation))
            
            rows = cursor.fetchall()  # This will fetch all matching rows
           # print(rows)
            # Create a list of objects with the required fields (discrepancy, parameters_num, best_model)
            results = [
                {
                    "discrepancy": row["discrepancy"],
                    "parameters_num": row["parameters_num"],
                    "best_model": bool(row["best_model"])  # Ensure this is converted to a boolean
                }
                for row in rows
            ]

            return results

    except sqlite3.DatabaseError as e:
        print(f"Database error while retrieving discrepancies: {e}")
        return []
    except Exception as e:
        print(f"Error retrieving discrepancies: {e}")
        return []
    finally:
        conn.close()


def get_genome_by_id(genome_id: int) -> Genome:
    db_path = get_db_path()  # Assuming this function gives the correct path to the database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This ensures rows are returned as dictionaries

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Genome WHERE id = ?", (genome_id,))
            row = cursor.fetchone()  # This will return a Row object (which behaves like a dictionary)
            
            if row:
                
                # Assuming 'functions' is stored as a JSON string in the database
                functions_data = json.loads(row["functions"])  # Now you can access by column name
                
                # Convert the functions data to actual Function objects
                functions = [Function.from_dict(func_data) for func_data in functions_data]
                #print(row)
                # Create and return the Genome instance with all required fields
                genome = Genome(
                    #id=row["id"],  # Assuming 'id' is the first column
                    #run=row["run"],
                    #generation=row["generation"],
                    fitness=row["fitness"],
                    discrepancy=row["discrepancy"],
                    area_penalty=row["area_penalty"],
                    peakes_width_penalty=row["peakes_width_penalty"],
                    peakes_num_penalty=row["peakes_num_penalty"],
                    free_parameters_penalty=row["free_parameters_penalty"],
                    compatibility_penalty=row["compatibility_penalty"],
                    best_model=bool(row["best_model"]),  # Ensure this is converted to a boolean
                    functions=functions
                )
                return genome, row["run"], row["generation"]
            else:
                return None, None, None  # Genome with the given id does not exist
    except sqlite3.DatabaseError as e:
        print(f"Database error while retrieving genome: {e}")
        return None, None, None
    except Exception as e:
        print(f"Error retrieving genome: {e}")
        return None, None, None
    finally:
        conn.close()


def get_generation_best_genome(run: int, generation: int) -> Genome | None:
    db_path = get_db_path()
    print(db_path)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    
    # Create a mapping from func_type to the actual class
    func_type_to_class = {
        FunctionType.PsuedoDelta: PseudoDelta,
        FunctionType.Gaussian: Gaussian,
        FunctionType.Lorentzian: Lorentzian,
        FunctionType.HyperbolicSecant: HyperbolicSecant,
        FunctionType.ColeCole: ColeCole,
        FunctionType.KirkwoodFuoss: KirkwoodFuoss,
        FunctionType.PearsonVII: PearsonVII,
        FunctionType.Losev: Losev,
        FunctionType.HavriliakNegami: HavriliakNegami,
        FunctionType.AsymmetricGaussian: AsymmetricGaussian,
        FunctionType.AsymmetricLorentzian: AsymmetricLorentzian,
        FunctionType.AsymmetricHyperbolicSecant: AsymmetricHyperbolicSecant,
        FunctionType.PseudoVoigt: PseudoVoigt
    }
    
    with conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Genome WHERE run = ? AND generation = ? AND best_model = 1''', (run, generation))
        row = cursor.fetchone()
        
        if row is None:
            print('no row found')
            return None  # Return None if no matching genome is found
        
        # Deserialize the functions and create the appropriate function subclass
        functions_data = json.loads(row[11])  # Get serialized functions
        functions = []
        
        for func_data in functions_data:
            func_type = FunctionType(func_data['func_type'])  # Get the function type
            func_class = func_type_to_class.get(func_type)  # Get the correct class for the function type
                
            if func_class:  # Check if a class is found
                # Directly pass the parameters dictionary to the function class
                function = func_class(func_data)  # Pass the params dictionary to the function class constructor
                
                # Append the created function to the list
                functions.append(function)
        
        genome = Genome(
            run=row[1],
            generation=row[2],
            fitness=row[3],
            discrepancy=row[4],
            area_penalty=row[5],
            peakes_width_penalty=row[6],
            peakes_num_penalty=row[7],
            free_parameters_penalty=row[8],
            compatibility_penalty=row[9],
            best_model=bool(row[10]),
            functions=functions
        )
    
    return genome




