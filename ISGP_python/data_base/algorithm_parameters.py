import json
import sqlite3
from file_managment.file_manager import get_db_path
from models.project import AlgorithmParameters
from models.functions.function import FunctionType

def create_algorithm_parameters_table():
    db_path = get_db_path()  # Ensure this returns the correct database path
    conn = sqlite3.connect(db_path, check_same_thread=False)
    
    try:
        with conn:
            cursor = conn.cursor()
            
            # Create the table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS algorithm_parameters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    runs_num INTEGER DEFAULT 3,
                    max_generations INTEGER DEFAULT 100,
                    mutate_probability REAL DEFAULT 0.5,
                    add_probability REAL DEFAULT 0.25,
                    stop_criteria INTEGER DEFAULT 10,
                    expected_peaks_num INTEGER DEFAULT 3,
                    norm_factor REAL DEFAULT 0.05,
                    point_diff REAL DEFAULT 3,
                    width_factor REAL DEFAULT 8,
                    alpha REAL DEFAULT 0.8,
                    w0 REAL DEFAULT 0.001,  
                    w1 REAL DEFAULT 0.0001, 
                    use_filter BOOLEAN DEFAULT False,       
                    population_size INTEGER DEFAULT 20,
                    initial_functions TEXT DEFAULT '[]',
                    mutation_functions TEXT DEFAULT '[]',
                    upper_bounds TEXT DEFAULT '{}',
                    lower_bounds TEXT DEFAULT '{}'
                )
            ''')

            # Check if there is already a row
            cursor.execute("SELECT COUNT(*) FROM algorithm_parameters")
            row_count = cursor.fetchone()[0]

            # Insert default row only if the table is empty
            if row_count == 0:
                cursor.execute('''
                    INSERT INTO algorithm_parameters (
                        runs_num, max_generations, mutate_probability, add_probability, 
                        stop_criteria, expected_peaks_num, norm_factor, point_diff, 
                        width_factor, alpha, w0, w1, use_filter, population_size, 
                        initial_functions, mutation_functions, upper_bounds, lower_bounds
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (3, 100, 0.5, 0.25, 10, 3, 0.05, 3, 8, 0.8, 0.001, 0.0001, False, 20, '', '', '{}', '{}'))

        return "Table created successfully and default row inserted if needed."
    except sqlite3.Error as e:
        return f"An error occurred: {e}"
    finally:
        conn.close()

def save_algorithm_parameters_to_db(params: AlgorithmParameters):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)

    try:
        with conn:
            cursor = conn.cursor()

            # Convert lists and dictionaries to text/JSON
            initial_functions_text = ','.join(str(item.value) for item in params.initial_functions)
            mutation_functions_text = ','.join(str(item.value) for item in params.mutation_functions)
            upper_bounds_text = json.dumps({ft.value: v for ft, v in params.upper_bounds.items()})
            lower_bounds_text = json.dumps({ft.value: v for ft, v in params.lower_bounds.items()})

            # Update existing row (assuming it always exists)
            cursor.execute(''' 
                UPDATE algorithm_parameters
                SET runs_num = ?, max_generations = ?, mutate_probability = ?, add_probability = ?, 
                    stop_criteria = ?, expected_peaks_num = ?, norm_factor = ?, point_diff = ?, 
                    width_factor = ?, alpha = ?, population_size = ?, initial_functions = ?, 
                    mutation_functions = ?, upper_bounds = ?, lower_bounds = ?
                WHERE id = 1
            ''', (
                params.runs_num, params.max_generations, params.mutate_probability, params.add_probability,
                params.stop_criteria, params.expected_peaks_num, params.norm_factor, params.point_diff,
                params.width_factor, params.alpha, params.population_size, initial_functions_text,
                mutation_functions_text, upper_bounds_text, lower_bounds_text
            ))

            # Ensure update actually happened
            if cursor.rowcount == 0:
                raise ValueError("No row found in algorithm_parameters. The table may be uninitialized.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def save_filter_parameters(w0, w1, use_filter):
    """Updates the filter parameters (w0, w1, use_filter)."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)

    try:
        with conn:
            cursor = conn.cursor()

            # Dynamically build the update query
            update_fields = []
            values = []

            if w0 is not None:
                update_fields.append("w0 = ?")
                values.append(w0)
            if w1 is not None:
                update_fields.append("w1 = ?")
                values.append(w1)
            if use_filter is not None:
                update_fields.append("use_filter = ?")
                values.append(use_filter)

            if update_fields:
                cursor.execute(f'''
                    UPDATE algorithm_parameters
                    SET {', '.join(update_fields)}
                    WHERE id = 1
                ''', values)

                # Ensure update actually happened
                if cursor.rowcount == 0:
                    raise ValueError("No row found in algorithm_parameters. The table may be uninitialized.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

    return "Filter parameters updated successfully."


            
def get_algorithm_parameters_from_db() -> AlgorithmParameters:
    db_path = get_db_path()
    print(db_path)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM algorithm_parameters LIMIT 1')
        row = cursor.fetchone()

        if row:
            print('found row')
            (id, runs_num, max_generations, mutate_probability, add_probability, stop_criteria, expected_peaks_num, norm_factor, point_diff,
             width_factor, alpha,w0,w1,use_filter, population_size, initial_functions_text, mutation_functions_text, upper_bounds_text, lower_bounds_text) = row
            print(population_size)
            print(use_filter)
            print(initial_functions_text)
            
            initial_functions = list(map(int, initial_functions_text.split(','))) if initial_functions_text else []
            mutation_functions = list(map(int, mutation_functions_text.split(','))) if mutation_functions_text else []
            upper_bounds = json.loads(upper_bounds_text) if upper_bounds_text else {}
            lower_bounds = json.loads(lower_bounds_text) if lower_bounds_text else {}

            # Convert keys back to FunctionType
            upper_bounds = {FunctionType(int(k)): v for k, v in upper_bounds.items()}
            lower_bounds = {FunctionType(int(k)): v for k, v in lower_bounds.items()}

            return AlgorithmParameters(
                runs_num=runs_num,
                max_generations=max_generations,
                mutate_probability=mutate_probability,
                add_probability=add_probability,
                stop_criteria=stop_criteria,
                expected_peaks_num=expected_peaks_num,
                norm_factor=norm_factor,
                point_diff=point_diff,
                width_factor=width_factor,
                alpha=alpha,
                population_size=population_size,
                initial_functions=initial_functions,
                mutation_functions=mutation_functions,
                upper_bounds=upper_bounds,
                lower_bounds=lower_bounds,
                
                use_filter=use_filter,
                w0=w0,
                w1=w1
            )
        else:
            return None
